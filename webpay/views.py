from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

API_URL = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions"
HEADERS = {
    "Tbk-Api-Key-Id": "597020000540",
    "Tbk-Api-Key-Secret": "XyZ12345",
    "Content-Type": "application/json"
}

@csrf_exempt
def webpay_init_transaction(request):
    if request.method == 'POST':
        data = {
            "buy_order": "orden1234",
            "session_id": "usuario123",
            "amount": 10000,
            "return_url": "http://localhost:8000/api/webpay/return/"
        }
        response = requests.post(API_URL, json=data, headers=HEADERS)
        try:
            result = response.json()
        except Exception:
            result = response.text
        return JsonResponse({
            "status_code": response.status_code,
            "result": result
        })
    else:
        return JsonResponse({'detail': 'Método no permitido'}, status=405)

@csrf_exempt
def webpay_return(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return JsonResponse({'error': 'No token_ws recibido'}, status=400)

    url = f"{API_URL}/{token_ws}"
    response = requests.put(url, headers=HEADERS)
    try:
        result = response.json()
    except Exception:
        result = response.text
    return JsonResponse({
        "status_code": response.status_code,
        "result": result
    })
