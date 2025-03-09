from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
        null=False
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=1000,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        default=1
    )
    price = models.DecimalField(
        verbose_name='Цена',
        validators=[MinValueValidator(0)],
        null=False,
        max_digits=10,
        decimal_places=2
    )
    base_price = models.DecimalField(
        verbose_name='Оптовая цена',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2
    )
    modified_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"[{self.id}] {self.name}"