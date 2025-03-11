from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Table(models.Model):
    # id - Номер стола.
    # Первичный ключ.
    # Проверка на > 0
    # Для unique ошибки есть текст.
    id = models.IntegerField(
        verbose_name='Номер стола',
        primary_key=True,
        validators=[MinValueValidator(1)],
        error_messages={'unique': 'Стол с таким номером уже существует!'},
    )
    # Название - Название стола. Не может быть пустым
    name = models.CharField(
        verbose_name='Наименование',
        max_length=100,
        null=False
    )
    # Кол-во стульев - По умолчанию 1. Должно >= 0
    chairs_counts = models.IntegerField(
        verbose_name='Кол-во стульев',
        validators=[MinValueValidator(0)],
        default=1
    )
    # Описание - Может быть пустым, ограничение 1000 символов
    description = models.CharField(
        verbose_name='Описание',
        max_length=1000,
        null=True,
        blank=True,
    )
    # Свободен? - По умолчанию свободен(True)
    is_available = models.BooleanField(
        verbose_name='Свободен',
        default=True,
    )
    # Обслуживает? - По умолчанию свободен(True)
    is_maintenance = models.BooleanField(
        verbose_name='Обслуживает',
        default=True,
    )
    # Дата изменения
    modified_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"#{self.id} {self.name}"
