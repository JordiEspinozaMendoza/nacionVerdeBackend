from rest_framework import serializers
from base.models import Products, Categories
from base.serializers.categories import CategoriesSerializer


class ProductsSerializer(serializers.ModelSerializer):
    categorie = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Products
        fields = "__all__"

    def get_categorie(self, obj):
        return CategoriesSerializer(obj.categorie, many=False).data
