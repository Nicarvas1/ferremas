from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def send_whatsapp_template(request):
    ACCESS_TOKEN = "EAAJ6QiuyAKkBO4dzjszaKUmjpY1ApqVS1ZCD58IHeZBvEZCh5AzbvMSyBMbnugtK2YhZCZBqLqWYZAaFIDG9n8WxHIVT9EtZAppgGCjRJ2zMJrGmmVFlhF6coHs4y3PYs71ZAaqReunlUwyw4i8xgImSBOv0ppnQAnIiDtabbmq2SfXN2xYMXzHZBMRDnIs7o7BCkMyilwNa8EKUfaQcos8RWrT2eSAZDZD"
    PHONE_NUMBER_ID = "626298767238639"
    RECIPIENT_NUMBER = "56955267084"  # Sin +

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_NUMBER,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return JsonResponse({"status": response.status_code, "result": response.json()})
