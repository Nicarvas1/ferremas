from rest_framework import serializers
from .models import Pedido, ItemPedido
from inventario.models import Producto
from inventario.serializers import ProductoSerializer

class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', write_only=True)

    class Meta:
        model = ItemPedido
        fields = ('id', 'producto', 'producto_id', 'cantidad')

class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ('id', 'usuario', 'fecha', 'estado', 'items')
