from django.db import models
from django.utils import timezone

# Create your models here.
class Categories(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    image = models.ImageField(
        upload_to="images/categories", blank=True, null=True, default=None
    )


class Products(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    price = models.FloatField(blank=True, null=True, default=0.0)
    description = models.TextField(blank=True, null=True, default="")
    image = models.ImageField(
        upload_to="images/products", blank=True, null=True, default=""
    )
    quantityStock = models.IntegerField(blank=True, null=True, default=0)
    isPublic = models.BooleanField(blank=True, null=True, default=True)
    categorie = models.ForeignKey(
        Categories, on_delete=models.CASCADE, blank=True, null=True, default=None
    )


class Customers(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    lastName = models.CharField(max_length=100, blank=True, null=True, default="")
    email = models.EmailField(blank=True, null=True, default="")
    phone = models.CharField(max_length=100, blank=True, null=True, default="")


class Orders(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    datePurchase = models.DateTimeField(default=timezone.now)
    total = models.FloatField(blank=True, null=True, default=0.0)
    status = models.BooleanField(blank=True, null=True, default=True)
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, blank=True, null=True, default=None
    )


class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    total = models.FloatField(blank=True, null=True, default=0.0)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, blank=True, null=True, default=None
    )


class Donations(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    dateDonation = models.DateTimeField(default=timezone.now)
    total = models.FloatField(blank=True, null=True, default=0.0)
    optionPay = models.CharField(max_length=100, blank=True, null=True, default="")
    quantity = models.IntegerField(blank=True, null=True, default=0)
    customer = models.ForeignKey(
        Customers, on_delete=models.CASCADE, blank=True, null=True, default=None
    )


class Solutions(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    short_description = models.TextField(blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True, default="")
    image = models.CharField(max_length=255, blank=True, null=True, default="")
    type = models.CharField(max_length=100, blank=True, null=True, default="")
    benefit_1 = models.TextField(blank=True, null=True, default="")
    benefit_2 = models.TextField(blank=True, null=True, default="")
    benefit_3 = models.TextField(blank=True, null=True, default="")

    data_1 = models.TextField(blank=True, null=True, default="")
    data_2 = models.TextField(blank=True, null=True, default="")
    data_3 = models.TextField(blank=True, null=True, default="")
    data_4 = models.TextField(blank=True, null=True, default="")

    phrase = models.TextField(blank=True, null=True, default="")
    phrase_author = models.TextField(blank=True, null=True, default="")
    icon = models.CharField(max_length=100, blank=True, null=True, default="")
