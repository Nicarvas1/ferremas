from django.urls import path
from .views import enviar_whatsapp_pedido

urlpatterns = [
    path('send/', enviar_whatsapp_pedido, name='enviar_whatsapp_pedido'),
]
