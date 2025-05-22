from django.urls import path
from .views import paypal_create_order, paypal_capture_order
from . import views


urlpatterns = [
    path("crear-orden/<str:total_usd>/", views.paypal_create_order, name="crear_orden_paypal"),
    path("capture-order/", views.paypal_capture_order, name="capture_order_paypal"),
]
