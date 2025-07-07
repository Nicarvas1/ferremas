from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = router.urls

handler404 = 'core.views.custom_404_view'
handler500 = 'core.views.custom_500_view'
