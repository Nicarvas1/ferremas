# core/context_processors.py

from inventario.models import Producto

def carrito_context(request):
    carrito = request.session.get('carrito', {})
    productos_dict = {str(p.id): p for p in Producto.objects.all()}
    total = 0
    total_productos = 0
    for pid, cantidad in carrito.items():
        prod = productos_dict.get(str(pid))
        if prod:
            total += prod.precio * cantidad
            total_productos += cantidad
    return {
        'carrito': carrito,
        'productos_dict': productos_dict,
        'total_carrito': total,
        'total_productos': total_productos,
    }
