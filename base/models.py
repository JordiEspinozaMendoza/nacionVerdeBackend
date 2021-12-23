from django.db import models

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
