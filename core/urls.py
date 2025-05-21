from django.urls import path, include
from django.contrib import admin
from . import views
from .views import webpay_init_transaction, webpay_return


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

]