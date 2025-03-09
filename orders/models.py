from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F

from products.models import Product
from tables.models import Table


# Create your models here.
class Order(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    table_number = models.OneToOneField(
        Table,
        on_delete=models.DO_NOTHING,
        related_name='order',
        verbose_name='Номер столика',
    )
    items = models.ManyToManyField(
        Product,
        through='OrderItem',
        related_name='orders',
        verbose_name='Продукты',
    )
    description = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='Описание',
    )

    STATUS_CHOICES = (
        ("PENDING", "В ожидании"),
        ("COMPLETED", "Готово"),
        ("PAID", "Оплачено"),
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    modified_date = models.DateTimeField(
        auto_now=True
    )
    total_price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    total_base_price = models.DecimalField(
        verbose_name='Оптовая цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"[{self.id}] {self.table_number} - {self.status}"

    def calculate_total_price(self):
        total = self.order_items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0
        return total

    def calculate_total_base_price(self):
        total = self.order_items.aggregate(
            total=Sum(F('product__base_price') * F('quantity'))
        )['total'] or 0
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
