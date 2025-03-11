from django.forms import ModelForm
from django.forms import Textarea

from .models import Table


# Форма создания стола
class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = ['id', 'name', 'chairs_counts', 'description', 'is_maintenance']
        widgets = {
            'description': Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            # Для каждого input-а даем bootstrap класс для стиля
            visible.field.widget.attrs['class'] = 'form-control'

        # Для не required описания убираем проверку.
        self.fields['description'].required = False
        # is_maintenance это чекбокс. Убираем класс form-control
        self.fields['is_maintenance'].widget.attrs['class'] = ''