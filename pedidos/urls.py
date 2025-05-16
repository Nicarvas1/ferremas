from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, ItemPedidoViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'items', ItemPedidoViewSet)

urlpatterns = router.urls
