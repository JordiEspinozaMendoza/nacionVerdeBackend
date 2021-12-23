from django import urls
from django.urls import path
from base.views import categories

urlpatterns = [
    path("", categories.getAll),
    path("create/", categories.post),
    path("<int:pk>/", categories.get),
    path("update/<int:pk>/", categories.put),
    path("delete/<int:pk>/", categories.delete),
]
