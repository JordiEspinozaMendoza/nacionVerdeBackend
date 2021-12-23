from django import urls
from django.urls import path
from base.views import products

urlpatterns = [
    path("", products.getAll),
    path("cart/", products.getCartProducts),
    path("create/", products.post),
    path("<int:pk>/", products.get),
    path("update/<int:pk>/", products.put),
    path("delete/<int:pk>/", products.delete),
]
