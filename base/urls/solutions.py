from django import urls
from django.urls import path
from base.views import solutions

urlpatterns = [
    path("", solutions.getAll),
    path("create/", solutions.post),
    path("<str:pk>/", solutions.get),
    path("update/<str:pk>/", solutions.put),
    path("delete/<str:pk>/", solutions.delete),
]
