from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    # id - автоген
    id = models.AutoField(
        primary_key=True
    )
    # Наименование - не может быть пустым. Лимит 100
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
        null=False
    )
    # Описание - Может быть пустым, ограничение 1000 символов
    description = models.CharField(
        verbose_name='Описание',
        max_length=1000,
        null=True,
        blank=True,
    )
    # Количество - По умолчанию 1
    quantity = models.IntegerField(
        verbose_name='Количество',
        default=1
    )
    # Цена - Пустым не может быть. Минимальное значение >= 0
    price = models.DecimalField(
        verbose_name='Цена',
        validators=[MinValueValidator(0)],
        null=False,
        max_digits=10,
        decimal_places=2
    )
    # Оптовая цена - Пустым может быть. Минимальное значение >= 0
    base_price = models.DecimalField(
        verbose_name='Оптовая цена',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2
    )
    # Дата изменения
    modified_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"[{self.id}] {self.name}"