from rest_framework import serializers
from base.models import Reports


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = "__all__"
