from django.shortcuts import render
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def webpay_init_transaction(request):
    tx = Transaction(
        commerce_code='597020000540',  # Código de comercio de prueba
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'  # ambiente de pruebas
    )
    buy_order = 'orden1234'
    session_id = 'usuario123'
    amount = 10000  # monto de prueba
    return_url = 'http://localhost:8000/api/webpay/return/'  # Donde volverá el usuario tras pagar

    response = tx.create(buy_order, session_id, amount, return_url)
    # Esto te devuelve una URL (redirect_url) donde debes redirigir al usuario para que pague en Webpay
    return JsonResponse({
        "url": response['url'],
        "token": response['token']
    })

def webpay_return(request):
    token = request.GET.get('token_ws')
    tx = Transaction(
        commerce_code='597020000540',
        api_key='022c0a599bfa4bc0a7a5e5c3a5e5c3a5',
        environment='TEST'
    )
    result = tx.commit(token)
    # Aquí puedes revisar el resultado y mostrarlo en pantalla o guardar el pago
    return JsonResponse(result)
