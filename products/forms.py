from django.forms import ModelForm
from django.forms import Textarea

from .models import Product


# Форма создания продукта
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            # Для каждого input-а даем bootstrap класс для стиля
            visible.field.widget.attrs['class'] = 'form-control'

        # Для не required полей убираем проверку.
        self.fields['description'].required = False
        self.fields['base_price'].required = False