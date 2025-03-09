from django.forms import ModelForm
from django.forms import Textarea

from .models import Order, OrderItem
from tables.models import Table

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'description']
        widgets = {
            'description': Textarea(attrs={'rows': 3,}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table_number'].queryset = Table.objects.filter(is_available=True, is_maintenance=True)
        self.fields['description'].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
