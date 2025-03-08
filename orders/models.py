from django.db import models

from products.models import Product
from tables.models import Table


# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    description = models.CharField(max_length=1000)
    total_price = models.FloatField(default=0)

    STATUS_CHOICES = (
        ("PENDING", "в ожидании"),
        ("COMPLETED", "готово"),
        ("PAID", "оплачено"),
    )
    status = models.CharField(max_length=9,
                              choices=STATUS_CHOICES,
                              default="PENDING")
