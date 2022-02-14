from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Products, Orders, OrderItem, Customers
from base.serializers.products import ProductsSerializer
from base.serializers.orders import OrderSerializer
from rest_framework import status
from datetime import datetime

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
import os


@api_view(["POST"])
def addOrderItems(request):
    try:
        data = request.data

        orderItems = data["orderItems"]
        customerData = data["customer"]
        if orderItems and len(orderItems) == 0:
            return Response(
                {"detail": "No Order Items", status: status.HTTP_400_BAD_REQUEST}
            )
        else:
            # (1) Create order
            order = Orders.objects.create(
                total=0.0,
                status=True,
            )
            if Customers.objects.filter(email=customerData["email"]).exists():
                customer = Customers.objects.get(email=customerData["email"])
                customer.name = customerData["name"]
                customer.phone = customerData["phone"]
                customer.lastName = customerData["lastName"]
                customer.age = customerData["age"]
                customer.wantsToReceiveEmails = customerData["wantsToReceiveEmails"]
                customer.gender = customerData["gender"]
                customer.save()
                order.customer = Customers.objects.get(email=customerData["email"])
            else:
                newCustomer = Customers.objects.create(
                    name=customerData["name"],
                    lastName=customerData["lastName"],
                    age=customerData["age"],
                    gender=customerData["gender"],
                    email=customerData["email"],
                    phone=customerData["phone"],
                    wantsToReceiveEmails=customerData["wantsToReceiveEmails"],
                )
                order.customer = newCustomer

            # (2) Create order items and set order to orderItem relationship
            for i in orderItems:
                if Products.objects.filter(_id=i["_id"]).exists():
                    product = Products.objects.get(_id=i["_id"])
                    item = OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=i["quantity"],
                        total=i["quantity"] * product.price,
                    )
                    # (3) Update stock
                    product.quantityStock -= item.quantity
                    product.save()
                    # (4) Update total
                    order.total += item.total
                    order.save()
            # * Send email
            orderItemsDict = []
            for i in orderItems:
                product = Products.objects.get(_id=i["_id"])
                orderItemsDict.append(
                    {
                        "name": product.name,
                        "price": product.price,
                        "quantity": i["quantity"],
                        "total": i["quantity"] * product.price,
                    }
                )
            template = render_to_string(
                "order.html",
                {
                    "name": customerData["name"],
                    "lastName": customerData["lastName"],
                    "email": customerData["email"],
                    "phone": customerData["phone"],
                    "orderItems": orderItemsDict,
                    "total": order.total,
                    "date": datetime.now(),
                },
            )

            email = EmailMultiAlternatives(
                "Detalles de orden",
                template,
                os.environ.get("EMAIL_CLIENT"),
                ["jordi.espinoza193@tectijuana.edu.mx"],
            )
            email.attach_alternative(template, "text/html")

            email.fail_silently = False
            email.send()
            serializer = OrderSerializer(order, many=False)

            return Response(serializer.data)

    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrders(request):
    orders = Orders.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getOrderById(request, pk):
    user = request.user
    order = Orders.objects.get(_id=pk)
    try:
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
    except:
        return Response(
            {"detail": "Order does not exists", status: status.HTTP_400_BAD_REQUEST}
        )
