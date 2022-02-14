from rest_framework.response import Response
from base.models import Reports
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, authentication, permissions
from base.serializers.reports import ReportsSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMultiAlternatives
import os
from django.template.loader import render_to_string

import django_excel as excel


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getExcel(request):
    try:
        export = []
        reports = Reports.objects.all()
        export.append(
            ["ID", "Nombre", "Correo", "Teléfono", "Fecha registro", "Contexto", "Tipo"]
        )
        for report in reports:
            typeReport = ""
            if report.type == "report":
                typeReport = "Denuncia"
            else:
                typeReport = "Reforestación"
            export.append(
                [
                    report._id,
                    report.name,
                    report.email,
                    report.phone,
                    report.date,
                    report.context,
                    typeReport,
                ]
            )
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, "csv", file_name="reports.xls")

    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportsView(APIView):
    def get(self, request):
        try:
            reports = Reports.objects.all()
            serializer = ReportsSerializer(reports, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            serializer = ReportsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                type = ""
                if data["type"] == "report":
                    type = "Denuncia"
                else:
                    type = "Reforestación de terreno"
                template = render_to_string(
                    "report.html",
                    {
                        "name": data["name"],
                        "city": data["city"],
                        "email": data["email"],
                        "context": data["context"],
                        "type": type,
                        "phone": data["phone"],
                    },
                )
                email = EmailMultiAlternatives(
                    type,
                    template,
                    os.environ.get("EMAIL_CLIENT"),
                    [data["email"], os.environ.get("EMAIL_CLIENT")],
                )
                email.attach_alternative(template, "text/html")
                if (
                    data["image"] != "null"
                    and data["image"] != ""
                    and data["image"] != "null"
                ):
                    imageReport = request.FILES["image"]
                    email.attach(
                        imageReport.name, imageReport.read(), imageReport.content_type
                    )

                email.fail_silently = False
                email.send()
                return Response(
                    {"message": "Successfully created"}, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
