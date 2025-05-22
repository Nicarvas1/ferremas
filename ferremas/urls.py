from django.contrib import admin
from django.urls import path, include

"""
URL configuration for ferremas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_csrf(request):
    return JsonResponse({"test": "funciona sin csrf"})



urlpatterns = [
    path('api/webpay/', include('webpay.urls')),
    path('api/paypal/', include(('paypal.urls', 'paypal'), namespace='paypal')),
    path('prueba-csrf/', test_csrf),  # pon esto arriba de todo
    path('api/whatsapp/', include('whatsapp.urls')),
    path('api/geolocalizacion/', include('geolocalizacion.urls')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Incluye las URLs de la aplicación 'core'
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)