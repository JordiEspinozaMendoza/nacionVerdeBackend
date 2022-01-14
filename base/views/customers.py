from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Customers
from rest_framework import status
from base.serializers.customers import CustomersSerializer

import django_excel as excel


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getExcel(request):
    try:
        export = []
        customers = Customers.objects.all()
        export.append(["ID", "Nombre", "Correo", "Teléfono", "Fecha registro"])
        for customer in customers:
            export.append(
                [
                    customer._id,
                    customer.name,
                    customer.email,
                    customer.phone,
                    customer.dateRegister,
                ]
            )
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, "csv", file_name="customers.xlsx")

    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAll(request):
    try:
        items = Customers.objects.all()
        serializer = CustomersSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def get(request, pk):
    try:
        item = Customers.objects.get(_id=pk)
        serializer = CustomersSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def post(request):
    try:
        data = request.data
        if Customers.objects.filter(email=data["email"]).exists():
            return Response(
                {"error": "Correo ya registrado"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            item = Customers.objects.create(
                name=data["name"],
                lastName=data["lastName"],
                email=data["email"],
                phone=data["phone"],
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
        item = Customers.objects.get(_id=pk)

        item.name = data["name"]
        item.lastName = data["lastName"]
        item.email = data["email"]

        item.save()
        return Response({"message": "Successfully updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete(request, pk):
    try:
        item = Customers.objects.get(_id=pk)
        item.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
