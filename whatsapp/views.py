from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def enviar_whatsapp_pedido(nombre, pedido_id, numero_destino):
    ACCESS_TOKEN = "EAAJ6QiuyAKkBO0Ljr6uBaeRHj7DZCAbaUUKGaZCDRr4ngwjce0S7Ap1lTLwjLUj7fDOLiify2ASRRiHARhkhoeoxZCbza2OXRHn4Ugz3a0CmhueLktZAZAXKJ4MMAiWBQcN0GPO2HvZCUJHU80vFISQdZAlq6yx5GlVlZBVqoqEq5Wtfnk3wmDdMHBd1W1imG9ZBjBlpTpVRp7wNThJyZAxjE59CYyirdqqOocqfsxJmkZD"
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

