from django.urls import path
from .views import webpay_init_transaction, webpay_return

urlpatterns = [
    path('init/', webpay_init_transaction, name='webpay_init'),
    path('return/', webpay_return, name='webpay_return'),
]
