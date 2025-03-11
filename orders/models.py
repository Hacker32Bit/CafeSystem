from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F

from products.models import Product
from tables.models import Table


# Модель заказа
class Order(models.Model):
    # id - автоген
    id = models.AutoField(
        primary_key=True,
    )
    # table_number - 1 к 1. т.е. 1 заказ на 1 стол. При удалении ничего не делать
    table_number = models.OneToOneField(
        Table,
        on_delete=models.DO_NOTHING,
        related_name='order',
        verbose_name='Номер столика',
    )
    # items - Продукты много к многому. Т.е. на несколько заказов несколько товаров.
    items = models.ManyToManyField(
        Product,
        through='OrderItem',
        related_name='orders',
        verbose_name='Продукты',
    )
    # Описание - Может быть пустым, ограничение 1000 символов
    description = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    # Константы для выбора статуса
    STATUS_CHOICES = (
        ("PENDING", "В ожидании"),
        ("COMPLETED", "Готово"),
        ("PAID", "Оплачено"),
    )
    # Статус - Выбор статуса. По умолчанию "В ожидении"
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    # Дата создания заказа
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    # Дата изменения заказа
    modified_date = models.DateTimeField(
        auto_now=True
    )
    # Итоговая цена - Макс. кол-во чисел 10.
    # Делиметр до сотни.
    # По умолчанию 0.
    # Лимит >= 0
    total_price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    # Итоговая оптовая цена - Макс. кол-во чисел 10.
    # Делиметр до сотни.
    # По умолчанию 0.
    # Лимит >= 0
    total_base_price = models.DecimalField(
        verbose_name='Оптовая цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"[{self.id}] {self.table_number} - {self.status}"

    # Функция подсчета итоговой цены
    def calculate_total_price(self):
        total = self.order_items.aggregate(
            total=Sum(F('product__price') * F('quantity'))
        )['total'] or 0
        return total

    # Функция подсчета итоговой оптовой цены
    def calculate_total_base_price(self):
        total = self.order_items.aggregate(
            total=Sum(F('product__base_price') * F('quantity'))
        )['total'] or 0
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# Класс заказа 1го продукта
class OrderItem(models.Model):
    # Связь Order по ключу
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    # Связь Product по ключу
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    # Добавить для Item количество от 1-го и более
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
