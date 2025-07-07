from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50, blank=True)
    categoria = models.CharField(max_length=50, blank=True)
    foto = models.CharField(max_length=50, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class StockSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'sucursal')

    def __str__(self):
        return f"{self.producto.nombre} - {self.sucursal.nombre}: {self.cantidad}"
