from django.contrib import admin
from .models import Producto, Sucursal, StockSucursal

admin.site.register(Producto)
admin.site.register(Sucursal)
admin.site.register(StockSucursal)
