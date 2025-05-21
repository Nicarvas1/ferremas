# geolocalizacion/urls.py
from django.urls import path
from .views import geolocalizacion_ip

urlpatterns = [
    path('', geolocalizacion_ip, name='geolocalizacion_ip'),
]
