from django.db import models
from django.conf import settings
from inventario.models import Producto

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')  # pendiente, pagado, enviado, entregado, etc.
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, default='manual')
    datos_pago = models.JSONField(null=True, blank=True)  # para guardar respuesta paypal
    tipo_entrega = models.CharField(
        max_length=20,
        choices=[('retiro', 'Retiro en tienda'), ('despacho', 'Despacho a domicilio')],
        default='retiro'
    )
    direccion_entrega = models.CharField(max_length=255, blank=True, null=True)
    sucursal_retiro = models.CharField(max_length=100, blank=True, null=True)




class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
