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

from core import views as core_views

urlpatterns += [
    path('vendedor/', core_views.vista_pedidos_vendedor, name='vista_pedidos_vendedor'),
    path('vendedor/aprobar/<int:pedido_id>/', core_views.aprobar_pedido, name='aprobar_pedido'),
    path('vendedor/rechazar/<int:pedido_id>/', core_views.rechazar_pedido, name='rechazar_pedido'),
    path('vendedor/entregado/<int:pedido_id>/', core_views.marcar_entregado, name='marcar_entregado'),
    path('vendedor/historial/', core_views.historial_vendedor, name='historial_vendedor'),

]


urlpatterns += [
    path('bodeguero/', core_views.vista_pedidos_bodeguero, name='vista_pedidos_bodeguero'),
    path('bodeguero/preparar/<int:pedido_id>/', core_views.preparar_pedido, name='preparar_pedido'),
    path('bodeguero/preparado/<int:pedido_id>/', core_views.marcar_preparado, name='marcar_preparado'),
    path('bodeguero/historial/', core_views.historial_bodeguero, name='historial_bodeguero'),

]

urlpatterns += [
    path('contador/', core_views.vista_pedidos_contador, name='vista_pedidos_contador'),
    path('contador/confirmar/<int:pedido_id>/', core_views.confirmar_pago, name='confirmar_pago'),
    path('contador/historial/', core_views.historial_contador, name='historial_contador'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)