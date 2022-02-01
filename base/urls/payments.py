from django.urls import path
from base.views import payments

urlpatterns = [
    path("save-stripe-info/", payments.save_stripe_info),
    path("save-stripe-subscription-info/", payments.create_donation),
]
