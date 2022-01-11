from rest_framework import serializers
from base.models import Customers, Orders
from base.serializers.orderItem import OrderItemSerializer
from base.serializers.customers import CustomersSerializer


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    customer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_customer(self, obj):
        customer = obj.customer
        serializer = CustomersSerializer(customer, many=False)
        return serializer.data
