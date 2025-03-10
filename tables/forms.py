from django.forms import ModelForm
from django.forms import Textarea

from .models import Table


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
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['description'].required = False
        self.fields['is_maintenance'].widget.attrs['class'] = ''