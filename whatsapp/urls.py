from django.urls import path
from .views import send_whatsapp_template

urlpatterns = [
    path('send/', send_whatsapp_template, name='send_whatsapp_template'),
]
