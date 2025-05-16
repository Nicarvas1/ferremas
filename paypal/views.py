# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Tus credenciales de SANDBOX
CLIENT_ID = "AbGbDpjC3E9Is7_bbxtPBZya2HJW9cP023qlou3JdT7bzV9-tcbAEeSG03IkWgZoiylITjj4cSzLusUb"
CLIENT_SECRET = "EIxjIeDfs9NgxoCKHXysPbnRHLwkRnniuIpOAfu2YKb1nI5CjMlO62WlMLxyEpI0ihzSUOWhDc5rD6yU"
BASE_URL = "https://api-m.sandbox.paypal.com"

def get_paypal_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    response = requests.post(url,
                             headers={"Accept": "application/json", "Accept-Language": "en_US"},
                             data={"grant_type": "client_credentials"},
                             auth=(CLIENT_ID, CLIENT_SECRET))
    return response.json().get("access_token")

@csrf_exempt
def paypal_create_order(request):
    access_token = get_paypal_access_token()
    if not access_token:
        return JsonResponse({"error": "No se pudo obtener el token de acceso de PayPal"}, status=400)

    url = f"{BASE_URL}/v2/checkout/orders"
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": "10.00"
            }
        }],
        "application_context": {
            "return_url": "http://localhost:8000/api/paypal/capture-order/",
            "cancel_url": "http://localhost:8000/api/paypal/cancel/"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, json=order_data, headers=headers)
    data = resp.json()

    # Busca el link de "approve"
    approve_url = next((l["href"] for l in data["links"] if l["rel"] == "approve"), None)
    return JsonResponse({
        "order_id": data.get("id"),
        "approve_url": approve_url,
        "paypal_response": data
    })

@csrf_exempt
def paypal_capture_order(request):
    order_id = request.GET.get("token")  # PayPal retorna ?token= al return_url
    if not order_id:
        return JsonResponse({"error": "Falta el token de la orden"}, status=400)
    access_token = get_paypal_access_token()
    url = f"{BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    resp = requests.post(url, headers=headers)
    return JsonResponse(resp.json())
