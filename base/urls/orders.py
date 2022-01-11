from django import urls
from django.urls import path
from base.views import orders

urlpatterns = [
    path("", orders.getOrders),
    path("create/", orders.addOrderItems),
    path("<str:pk>/", orders.getOrderById),
]
