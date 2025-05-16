from rest_framework import viewsets
from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer, ItemPedidoSerializer
from rest_framework.permissions import IsAuthenticated

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.all()
    serializer_class = ItemPedidoSerializer
    permission_classes = [IsAuthenticated]
