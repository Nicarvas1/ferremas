from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from usuarios.forms import CustomUserCreationForm
from inventario.models import Producto  # importa el modelo desde inventario
import requests
from pedidos.models import Pedido



def pagar_carrito(request):
    # Recalcula el total del carrito en CLP
    carrito = request.session.get('carrito', {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    total = 0
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            total += prod.precio * cantidad

    # Obtén la tasa de conversión (puedes optimizar esto para no llamar dos veces)
    api_key = '04d347025e7b23c5e4e00963'
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/CLP/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('result') == 'success':
            clp_usd = data['conversion_rate']
            total_usd = round(float(total) * clp_usd, 2)
        else:
            total_usd = 0
    except Exception as e:
        total_usd = 0

    # Ahora llama a la creación de la orden en PayPal
    return redirect('crear_pago_paypal', monto_usd=total_usd)

def detalle_carrito(request):
    print("CARGANDO VISTA DETALLE CARRITO")  # <-- Agrega esto

    carrito = request.session.get('carrito', {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    total = 0
    items = []
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            subtotal = prod.precio * cantidad
            items.append({'producto': prod, 'cantidad': cantidad, 'subtotal': subtotal})
            total += subtotal

    api_key = 'aa71decde1f2c9ae01f64825'
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/CLP/USD'
    try:
        response = requests.get(url)
        data = response.json()
        print(data)  # <-- Debug
        if data.get('result') == 'success':
            clp_usd = data['conversion_rate']
            total_usd = round(float(total) * clp_usd, 2)
        else:
            clp_usd = None
            total_usd = None
    except Exception as e:
        print(e)
        clp_usd = None
        total_usd = None

    return render(request, "detalle_carrito.html", {
        "items": items,
        "total": total,
        "total_usd": total_usd,
        "clp_usd": clp_usd
    })


def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('productos_ferreteria')

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1  # Suma 1 si ya existe
    request.session['carrito'] = carrito
    return redirect('productos_ferreteria')  # Redirige de vuelta a la página de productos


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Listado único de categorías (como en la vista de productos)
    categorias = Producto.objects.values_list('categoria', flat=True).distinct().order_by('categoria')
    categoria_activa = request.GET.get('categoria', '')

    return render(request, "detalle_producto.html", {
        "producto": producto,
        "categorias": categorias,
        "categoria_activa": categoria_activa
    })

def productos_ferreteria(request):
    productos = Producto.objects.all()
    categorias = [
        "Herramientas Manuales",
        "Herramientas Eléctricas",
        "Materiales Básicos",
        "Acabados",
        "Equipos de Seguridad",
        "Tornillos y Anclajes",
        "Fijaciones y Adhesivos",
        "Equipos de Medición"
    ]
    categoria_activa = request.GET.get('categoria')
    if categoria_activa:
        productos = productos.filter(categoria=categoria_activa)

    carrito = request.session.get("carrito", {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    total = 0
    total_productos = 0
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            total += prod.precio * cantidad
            total_productos += cantidad

    return render(request, "productos.html", {
        "productos": productos,
        "categorias": categorias,
        "categoria_activa": categoria_activa,
        "productos_dict": productos_dict,
        "total_carrito": total,
        "total_productos": total_productos,
    })





def index(request):
    return render(request, 'index.html')

def webpay_init_transaction(request):
    tx = Transaction(
        commerce_code='597020000540',  # Código de comercio de prueba
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'  # ambiente de pruebas
    )
    buy_order = 'orden1234'
    session_id = 'usuario123'
    amount = 10000  # monto de prueba
    return_url = 'http://localhost:8000/api/webpay/return/'  # Donde volverá el usuario tras pagar

    response = tx.create(buy_order, session_id, amount, return_url)
    # Esto te devuelve una URL (redirect_url) donde debes redirigir al usuario para que pague en Webpay
    return JsonResponse({
        "url": response['url'],
        "token": response['token']
    })

def webpay_return(request):
    token = request.GET.get('token_ws')
    tx = Transaction(
        commerce_code='597020000540',
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'
    )
    result = tx.commit(token)
    # Aquí puedes revisar el resultado y mostrarlo en pantalla o guardar el pago
    return JsonResponse(result)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Usuario o contraseña inválidos.')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')

@login_required
def profile(request):
    pedidos_usuario = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'profile.html', {
        'user': request.user,
        'pedidos': pedidos_usuario
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from pedidos.models import Pedido

def es_vendedor(user):
    return user.is_authenticated and user.rol == 'vendedor'

@login_required
@user_passes_test(es_vendedor)
def vista_pedidos_vendedor(request):
    pedidos_pendientes = Pedido.objects.filter(estado='Pendiente')
    pedidos_preparados = Pedido.objects.filter(estado='Preparado')
    return render(request, 'vendedor/pedidos.html', {
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_preparados': pedidos_preparados
    })

@login_required
@user_passes_test(es_vendedor)
def aprobar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Aprobado'
    pedido.save()
    return redirect('vista_pedidos_vendedor')

@login_required
@user_passes_test(es_vendedor)
def rechazar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Rechazado'
    pedido.save()
    return redirect('vista_pedidos_vendedor')

@login_required
@user_passes_test(es_vendedor)
def marcar_entregado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Entregado'
    pedido.save()
    return redirect('vista_pedidos_vendedor')

@login_required
@user_passes_test(es_vendedor)
def historial_vendedor(request):
    pedidos = Pedido.objects.filter(estado__in=['Preparado', 'Entregado', 'Pagado', 'Rechazado'])
    return render(request, 'vendedor/historial.html', {'pedidos': pedidos})


def es_bodeguero(user):
    return user.is_authenticated and user.rol == 'bodeguero'

@login_required
@user_passes_test(es_bodeguero)
def vista_pedidos_bodeguero(request):
    pedidos = Pedido.objects.filter(estado__in=['Aprobado', 'En preparacion'])
    return render(request, 'bodeguero/pedidos.html', {'pedidos': pedidos})

@login_required
@user_passes_test(es_bodeguero)
def preparar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'En preparacion'
    pedido.save()
    return redirect('vista_pedidos_bodeguero')

@login_required
@user_passes_test(es_bodeguero)
def marcar_preparado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Preparado'
    pedido.save()
    return redirect('vista_pedidos_bodeguero')

@login_required
@user_passes_test(es_bodeguero)
def historial_bodeguero(request):
    pedidos = Pedido.objects.filter(estado__in=['Preparado', 'Entregado', 'Pagado'])
    return render(request, 'bodeguero/historial.html', {'pedidos': pedidos})


def es_contador(user):
    return user.is_authenticated and user.rol == 'contador'

@login_required
@user_passes_test(es_contador)
def vista_pedidos_contador(request):
    pedidos = Pedido.objects.filter(metodo_pago='Transferencia', estado='Entregado')
    return render(request, 'contador/pedidos.html', {'pedidos': pedidos})

@login_required
@user_passes_test(es_contador)
def confirmar_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = 'Pagado'
    pedido.save()
    return redirect('vista_pedidos_contador')

@login_required
@user_passes_test(es_contador)
def historial_contador(request):
    pedidos = Pedido.objects.filter(estado='Pagado')
    return render(request, 'contador/historial.html', {'pedidos': pedidos})
