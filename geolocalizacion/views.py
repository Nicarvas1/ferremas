# geolocalizacion/views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def geolocalizacion_ip(request):
    # Puedes cambiar ip-api por ipinfo si quieres (ver más abajo)
    ip = request.GET.get("ip", "8.8.8.8")  # Si no das IP, usa la de Google
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    return JsonResponse(response.json())
