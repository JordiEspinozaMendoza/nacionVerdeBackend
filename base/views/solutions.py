from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Solutions
from rest_framework import status
from base.serializers.solutions import SolutionsSerializer


@api_view(["GET"])
def getAll(request):
    try:
        items = Solutions.objects.all()
        serializer = SolutionsSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get(request, pk):
    try:
        item = Solutions.objects.get(_id=pk)
        serializer = SolutionsSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def post(request):
    try:
        data = request.data
        item = Solutions.objects.create(
            name=data["name"],
            short_description=data["short_description"],
            description=data["description"],
            type=data["type"],
            benefit_1=data["benefit_1"],
            benefit_2=data["benefit_2"],
            benefit_3=data["benefit_3"],
            data_1=data["data_1"],
            data_2=data["data_2"],
            data_3=data["data_3"],
            data_4=data["data_4"],
            phrase=data["phrase"],
            phrase_author=data["phrase_author"],
            icon=data["icon"],
            image=data["image"],
        )
        item.save()
        return Response(
            {"message": "Successfully created"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def put(request, pk):
    try:
        data = request.data
        item = Solutions.objects.get(_id=pk)
        item.name = data["name"]
        item.short_description = data["short_description"]
        item.description = data["description"]
        item.type = data["type"]
        item.benefit_1 = data["benefit_1"]
        item.benefit_2 = data["benefit_2"]
        item.benefit_3 = data["benefit_3"]
        item.data_1 = data["data_1"]
        item.data_2 = data["data_2"]
        item.data_3 = data["data_3"]
        item.data_4 = data["data_4"]
        item.phrase = data["phrase"]
        item.phrase_author = data["phrase_author"]
        item.icon = data["icon"]
        item.image = data["image"]
        item.save()
        return Response({"message": "Successfully updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete(request, pk):
    try:
        item = Solutions.objects.get(_id=pk)
        item.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
