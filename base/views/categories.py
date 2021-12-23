from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Categories
from rest_framework import status
from base.serializers.categories import CategoriesSerializer


@api_view(["GET"])
def getAll(request):
    try:
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get(request, pk):
    try:
        category = Categories.objects.get(_id=pk)
        serializer = CategoriesSerializer(category)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def post(request):
    try:
        data = request.data
        item = Categories.objects.create(
            name=data["name"],
            description=data["description"],
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
        item = Categories.objects.get(_id=pk)
        data = request.data
        item.name = data["name"]
        item.description = data["description"]
        if data["image"] is not None:
            item.image = data["image"]
        item.save()
        return Response({"message": "Successfully updated"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete(request, pk):
    try:
        categories = Categories.objects.get(_id=pk)
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
