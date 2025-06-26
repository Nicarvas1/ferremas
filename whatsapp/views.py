from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def enviar_whatsapp_pedido(nombre, pedido_id, numero_destino):
    ACCESS_TOKEN = "EAAJ6QiuyAKkBO9HGMo5iAJcYrtCnuV49RKNKTcK3ghmIiZBXmE57rY6XQ1fUZAPfnqd9OgKUO3eDpt5zWU8VwYgrKIQgGZATOaKzb8u5ZCn5snFDZCdLj5qk7isnSVGj44DfU9uPakx7vU7kwZB1tPdok1O6I10Jtggy9ZBfHjvByJ4RZArTr8Pvm7wE9WymhlUsA5rwrIAwmopqiub0DPLhRhbscdczWRIFTQZDZD"
    PHONE_NUMBER_ID = "626298767238639"
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "template",
        "template": {
            "name": "pedidos_id",  # Tu plantilla de Meta
            "language": {
                "code": "es"  # Ajusta según la plantilla (es, es_MX, etc)
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": nombre},
                        {"type": "text", "text": str(pedido_id)}
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()

