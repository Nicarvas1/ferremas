from django.urls import path
from .views import paypal_create_order, paypal_capture_order

urlpatterns = [
    path('create-order/', paypal_create_order, name='paypal_create_order'),
    path('capture-order/', paypal_capture_order, name='paypal_capture_order'),
]
