# views.py
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from pedidos.models import Pedido, ItemPedido
from inventario.models import Producto  # Asegúrate de que la ruta sea correcta
from usuarios.models import Usuario  # O la ruta real donde está tu modelo custom
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
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Usuario no autenticado"}, status=401)
    
        # 👇 Capturamos el tipo de entrega desde el POST
    if request.method == 'POST':
        tipo_entrega = request.POST.get('entrega')
        sucursal = request.POST.get('sucursal')
        direccion = request.POST.get('direccion')
        total = request.POST.get('total_clp')

        request.session['tipo_entrega'] = tipo_entrega
        request.session['sucursal'] = sucursal
        request.session['direccion'] = direccion
        request.session['total_clp'] = total  # total_clp = valor en pesos



    total_usd = float(total_usd)
    access_token = get_paypal_access_token()
    if not access_token:
        return JsonResponse({"error": "No se pudo obtener el token de acceso de PayPal"}, status=400)

    url = f"{BASE_URL}/v2/checkout/orders"  # <--- AGREGA ESTA LÍNEA AQUÍ

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": f"{total_usd:.2f}"
            },
            "custom_id": str(request.user.id)
        }],
        "application_context": {
            "return_url": "http://localhost:8000/api/paypal/capture-order/",
            "cancel_url": "http://localhost:8000/api/paypal/cancel/"
        }
    }

    print("JSON enviado a PayPal:", order_data)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, json=order_data, headers=headers)
    data = resp.json()
    print("Respuesta PayPal (crear orden):", data)
    approve_url = next((l["href"] for l in data["links"] if l["rel"] == "approve"), None)
    if approve_url:
        return redirect(approve_url)
    return JsonResponse({"error": "No se pudo generar la orden PayPal", "response": data}, status=400)

@csrf_exempt
def paypal_capture_order(request):
    tipo_entrega = request.session.get('tipo_entrega', 'retiro')
    sucursal = request.session.get('sucursal', '')
    direccion = request.session.get('direccion', '')
    total = request.session.get('total_clp', 0)
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
    print("Respuesta PayPal (capture):", data)

    # Nueva ruta para custom_id:
    custom_id = None
    try:
        custom_id = data['purchase_units'][0]['payments']['captures'][0]['custom_id']
    except Exception as e:
        print("No se encontró custom_id en la respuesta:", e)

    if custom_id:
        try:
            usuario = Usuario.objects.get(id=custom_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=401)
    else:
        return JsonResponse({"error": "No se pudo recuperar el usuario"}, status=401)

    # 1. Recuperar datos del carrito de la sesión
    carrito = request.session.get('carrito', {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    items = []
    total = 0  # Total en CLP
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            subtotal = prod.precio * cantidad
            items.append({'producto': prod, 'cantidad': cantidad, 'subtotal': subtotal})
            total += subtotal
            print("==== DEBUG PEDIDO ====")

    print("Carrito:", carrito)
    print("Total CLP calculado:", total)
    print("Items:", items)
    print("Usuario:", usuario)
    print("Tipo entrega:", tipo_entrega)
    print("Sucursal:", sucursal)
    print("Dirección:", direccion)


    # 2. Crear el pedido
    # if request.user.is_authenticated:
    #     usuario = request.user
    # else:
    #     usuario = None  # O maneja como usuario invitado

    pedido = Pedido.objects.create(
        usuario=usuario,
        total=total,
        estado='Pendiente',
        metodo_pago='PAYPAL',
        datos_pago=data,
        tipo_entrega=tipo_entrega,
        direccion_entrega=direccion,
        sucursal_retiro=sucursal
    )



    nombre = getattr(usuario, 'first_name', None) or getattr(usuario, 'nombre', None) or usuario.username or 'Usuario'
    numero = "56955267084"  # Usa uno real si existe
    print("Nombre:", nombre)
    print("Pedido ID:", pedido.id)
    print("Numero:", numero)

    # Llama a la función
    status, respuesta = enviar_whatsapp_pedido(nombre, pedido.id, numero)
    print("Whatsapp enviado:", status, respuesta)


    # 3. Crear los ítems
    for item in items:
        producto = item['producto']
        cantidad = item['cantidad']

        # Crear el item
        ItemPedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
        )

        # 👇 Descontar stock según tipo de entrega
        if tipo_entrega == 'despacho':
            producto.stock = max(0, producto.stock - cantidad)
            producto.save()
        elif tipo_entrega == 'retiro' and sucursal:
            from inventario.models import StockSucursal, Sucursal
            try:
                suc = Sucursal.objects.get(nombre=sucursal)
                stock_obj = StockSucursal.objects.get(producto=producto, sucursal=suc)
                stock_obj.cantidad = max(0, stock_obj.cantidad - cantidad)
                stock_obj.save()
            except (Sucursal.DoesNotExist, StockSucursal.DoesNotExist) as e:
                print(f" Error al descontar stock en sucursal: {e}")


    # 4. Limpiar carrito
    request.session['carrito'] = {}
    request.session.pop('tipo_entrega', None)
    request.session.pop('sucursal', None)
    request.session.pop('direccion', None)

    # 5. Mostrar comprobante
    return render(request, "boleta_paypal.html", {"pago": data, "pedido": pedido})


