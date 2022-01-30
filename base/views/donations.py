from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Donations, Customers
from rest_framework import status
from base.serializers.donations import DonationsSerializer
from datetime import date
from base.pdfUtils.main import createPdf

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import os
from django.template.loader import render_to_string


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAll(request):
    try:
        items = Donations.objects.all()
        serializer = DonationsSerializer(items, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def get(request, pk):
    try:
        item = Donations.objects.get(_id=pk).order_by("-_id")
        serializer = DonationsSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def create(request):
    try:
        data = request.data
        item = Donations.objects.create(
            total=data["price"],
            optionPay=data["optionPay"],
            quantity=data["quantity"],
        )
        if Customers.objects.filter(email=data["email"]).exists():
            item.customer = Customers.objects.get(email=data["email"])
        else:
            newCustomer = Customers.objects.create(
                name=data["name"],
                lastName=data["lastName"],
                email=data["email"],
                phone=data["phone"],
            )
            item.customer = newCustomer
        item.save()
        template = render_to_string(
                "certificate.html",
                {
                    "name": data["name"],
                    "lastName": data["lastName"],
                    "quantity": data["quantity"],
                },
            )
        email = EmailMultiAlternatives(
            "Certificado de donación",
            "",
            os.environ.get("EMAIL_CLIENT"),
            [data["email"]],
        )
        pdf = createPdf(f"{data['name']} {data['lastName']}", data["quantity"])
        email.attach_file(pdf, "application/pdf")
        email.attach_alternative(template, "text/html")
        email.send()
        # Delete pdf
        os.remove(pdf)
        serializer = DonationsSerializer(item)
        return Response(serializer.data)
    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
