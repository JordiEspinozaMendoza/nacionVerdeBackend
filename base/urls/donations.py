from django import urls
from django.urls import path
from base.views import donations

urlpatterns = [
    path("", donations.getAll),
    path("create/", donations.create),
]
