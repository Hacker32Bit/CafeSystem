from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    base_price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
