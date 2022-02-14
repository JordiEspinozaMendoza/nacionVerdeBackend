from django.urls import path
from base.views.reports import ReportsView
from base.views import reports as functions
urlpatterns = [
    path("", ReportsView.as_view(), name="reports"),
    path("excel/", functions.getExcel, name="reports"),
]
