import email
from click import confirm
import stripe
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

stripe.api_key = os.environ.get("STRIPE_API_KEY")


@api_view(["POST"])
def save_stripe_info(request):
    data = request.data
    email = data["email"]
    payment_method_id = data["payment_method_id"]
    extra_msg = ""  # add new variable to response message
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={"default_payment_method": payment_method_id}
        )
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."
    stripe.PaymentIntent.create(
        customer=customer,
        payment_method=payment_method_id,
        currency="mxn",
        amount=data["total"] * 100,
        confirm=True,
    )
    return Response(
        status=status.HTTP_200_OK,
        data={
            "message": "Success",
            "data": {"customer_id": customer.id, "extra_msg": extra_msg},
        },
    )


@api_view(["POST"])
def create_donation(request):
    data = request.data
    email = data["email"]
    payment_method_id = data["payment_method_id"]
    extra_msg = ""  # add new variable to response message
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data

    # if the array is empty it means the email has not been used yet
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."
    stripe.Subscription.create(
        customer=customer,
        items=[
            {"price": os.environ.get("STRIPE_PRODUCT"), "quantity": data["quantity"]},
        ],  # here paste your price id
    )
    return Response(
        status=status.HTTP_200_OK,
        data={
            "message": "Success",
            "data": {"customer_id": customer.id, "extra_msg": extra_msg},
        },
    )
