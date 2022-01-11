from rest_framework import serializers
from base.models import Solutions


class SolutionsSerializer(serializers.ModelSerializer):


    class Meta:
        model = Solutions
        fields = "__all__"


