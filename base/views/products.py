from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Products, Categories
from rest_framework import status
from base.serializers.products import ProductsSerializer


@api_view(["GET"])
def getAll(request):
    try:
        items = Products.objects.all()
        serializer = ProductsSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get(request, pk):
    try:
        item = Products.objects.get(_id=pk)
        serializer = ProductsSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def getCartProducts(request):
    try:
        data = request.data
        items = []
        for item in data:
            items.append(Products.objects.get(_id=item["id"]))

        serializer = ProductsSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def post(request):
    try:
        data = request.data
        item = Products.objects.create(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantityStock=data["stock"],
            isPublic=True if data["public"] == "true" else False,
            categorie=Categories.objects.get(_id=data["categorie"]),
        )
        if data["image"] is not None:
            item.image = data["image"]
        item.save()
        return Response(
            {"message": "Successfully created"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def put(request, pk):
    try:
        item = Products.objects.get(_id=pk)
        data = request.data
        item.name = data["name"]
        item.description = data["description"]
        item.price = data["price"]
        item.quantityStock = data["quantityStock"]
        item.isPublic = True if data["isPublic"] == "true" else False
        item.categorie = Categories.objects.get(_id=data["categorie"])

        if data["image"] is not None:
            item.image = data["image"]
        item.save()
        return Response({"message": "Successfully updated"}, status=status.HTTP_200_OK)

    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete(request, pk):
    try:
        item = Products.objects.get(_id=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
