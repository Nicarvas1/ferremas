# views.py
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from pedidos.models import Pedido, ItemPedido
from inventario.models import Producto  # Asegúrate de que la ruta sea correcta
from django.contrib.auth.models import User  # O tu modelo de usuario
from whatsapp.views import enviar_whatsapp_pedido

# Tus credenciales de SANDBOX
CLIENT_ID = "AbGbDpjC3E9Is7_bbxtPBZya2HJW9cP023qlou3JdT7bzV9-tcbAEeSG03IkWgZoiylITjj4cSzLusUb"
CLIENT_SECRET = "EIxjIeDfs9NgxoCKHXysPbnRHLwkRnniuIpOAfu2YKb1nI5CjMlO62WlMLxyEpI0ihzSUOWhDc5rD6yU"
BASE_URL = "https://api-m.sandbox.paypal.com"

def get_paypal_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    response = requests.post(url,
                             headers={"Accept": "application/json", "Accept-Language": "en_US"},
                             data={"grant_type": "client_credentials"},
                             auth=(CLIENT_ID, CLIENT_SECRET))
    return response.json().get("access_token")

@csrf_exempt
def paypal_create_order(request, total_usd):
    total_usd = float(total_usd)  # Convierte acá

    access_token = get_paypal_access_token()
    if not access_token:
        return JsonResponse({"error": "No se pudo obtener el token de acceso de PayPal"}, status=400)

    url = f"{BASE_URL}/v2/checkout/orders"
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{total_usd:.2f}"
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/api/paypal/capture-order/",
            "cancel_url": "http://localhost:8000/api/paypal/cancel/"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, json=order_data, headers=headers)
    data = resp.json()
    approve_url = next((l["href"] for l in data["links"] if l["rel"] == "approve"), None)
    if approve_url:
        return redirect(approve_url)
    return JsonResponse({"error": "No se pudo generar la orden PayPal", "response": data}, status=400)
@csrf_exempt
def paypal_capture_order(request):
    order_id = request.GET.get("token")
    if not order_id:
        return HttpResponse("Falta el token de la orden.", status=400)
    access_token = get_paypal_access_token()
    url = f"{BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.post(url, headers=headers)
    data = resp.json()

    # 1. Recuperar datos del carrito de la sesión
    carrito = request.session.get('carrito', {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    items = []
    total = 0
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            subtotal = prod.precio * cantidad
            items.append({'producto': prod, 'cantidad': cantidad, 'subtotal': subtotal})
            total += subtotal

    # 2. Crear el pedido
    if request.user.is_authenticated:
        usuario = request.user
    else:
        usuario = None  # O maneja como usuario invitado

    pedido = Pedido.objects.create(
        usuario=usuario,
        total=total,
        estado='PAGADO',  # O el estado que manejes
        metodo_pago='PAYPAL',
        datos_pago=data  # Si quieres guardar la respuesta entera, pon JSONField en el modelo
    )
    # Supón que tienes el nombre y el teléfono del usuario:
    nombre = usuario.first_name if usuario and usuario.first_name else 'Usuario'
    numero = usuario.telefono if usuario and hasattr(usuario, "telefono") else "56955267084"  # Usa uno real si existe

    # Llama a la función
    status, respuesta = enviar_whatsapp_pedido(nombre, pedido.id, numero)
    print("Whatsapp enviado:", status, respuesta)


    # 3. Crear los ítems
    for item in items:
        ItemPedido.objects.create(
            pedido=pedido,
            producto=item['producto'],
            cantidad=item['cantidad'],
        )

    # 4. Limpiar carrito
    request.session['carrito'] = {}

    # 5. Mostrar comprobante
    return render(request, "boleta_paypal.html", {"pago": data, "pedido": pedido})

