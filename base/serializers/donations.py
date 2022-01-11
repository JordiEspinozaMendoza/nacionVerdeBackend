from rest_framework import serializers
from base.models import Donations
from base.serializers.customers import CustomersSerializer


class DonationsSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Donations
        fields = "__all__"

    def get_customer(self, obj):

        return CustomersSerializer(obj.customer, many=False).data
