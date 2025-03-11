from django.forms import ModelForm
from django.forms import Textarea

from .models import Order, OrderItem
from tables.models import Table

# Форма для добавления товара в заказ
class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# Форма заказа
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'description']
        # Для description даем Textarea с размером 3
        widgets = {
            'description': Textarea(attrs={'rows': 3,}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтруем и отображаем номера столов те которые свободны и обслуживают
        self.fields['table_number'].queryset = Table.objects.filter(is_available=True, is_maintenance=True)
        # Для Description ставим не обязательный параметр
        self.fields['description'].required = False

        for visible in self.visible_fields():
            # Для всех форм даем класс из bootstrap-a для дизайна
            visible.field.widget.attrs['class'] = 'form-control'
