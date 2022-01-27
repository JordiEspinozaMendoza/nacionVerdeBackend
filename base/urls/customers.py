from django import urls
from django.urls import path
from base.views import customers

urlpatterns = [
    path("", customers.getAll),
    path("create/", customers.post),
    path("excel/", customers.getExcel),
    path("report/", customers.sendReport)
]
