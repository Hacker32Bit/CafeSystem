from django.forms import ModelForm
from django.forms import Textarea

from .models import Product


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
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['description'].required = False
        self.fields['base_price'].required = False