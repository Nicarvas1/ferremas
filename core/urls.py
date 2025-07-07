from django.urls import path, include
from django.contrib import admin
from . import views
from .views import crear_producto, eliminar_producto, webpay_init_transaction, webpay_return
from .views import productos_ferreteria



urlpatterns = [
    path('', views.index, name='index'),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/pedidos/', include('pedidos.urls')),
    path('api/webpay/init/', webpay_init_transaction, name='webpay_init'),
    path('api/webpay/return/', webpay_return, name='webpay_return'),
    path('api/webpay/', include('webpay.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('productos/', productos_ferreteria, name='productos_ferreteria'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.detalle_carrito, name='detalle_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/pagar/', views.pagar_carrito, name='pagar_carrito'),
    path('carrito/aumentar/<int:producto_id>/', views.aumentar_producto_carrito, name='aumentar_producto_carrito'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_producto_carrito, name='disminuir_producto_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('actualizar-stock-sucursal/<int:producto_id>/', views.actualizar_stock_sucursal, name='actualizar_stock_sucursal'),
    path('productos/nuevo/', crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

  




]