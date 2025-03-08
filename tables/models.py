from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Table(models.Model):
    id = models.IntegerField(verbose_name='Номер стола', error_messages={'unique': 'Стол с таким номером уже существует!'}, primary_key=True, validators=[MinValueValidator(1)])
    name = models.CharField(verbose_name='Наименование', max_length=100, null=False)
    chairs_counts = models.IntegerField(verbose_name='Кол-во стульев', validators=[MinValueValidator(0)], default=1)
    description = models.CharField(verbose_name='Описание', max_length=1000, null=True)

    def __str__(self):
        return f"[{self.id}] {self.name}"
