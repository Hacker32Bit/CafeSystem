from django.contrib import admin

from orders.models import Order
from products.models import Product
from tables.models import Table

# Register your models here.
admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Order)
