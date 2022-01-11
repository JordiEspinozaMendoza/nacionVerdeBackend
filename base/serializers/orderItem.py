from rest_framework import serializers
from base.models import Customers, OrderItem
from base.serializers.products import ProductsSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_product(self, obj):
        product = obj.product
        serializer = ProductsSerializer(product, many=False)
        return serializer.data
