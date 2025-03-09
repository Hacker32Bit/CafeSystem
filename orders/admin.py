from django.contrib import admin

from tables.models import Table
from .models import Order, OrderItem

# Unregister the existing Order model if it is already registered
admin.site.unregister(Order)

# Define inline for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'table_number', 'status', 'total_price']
    list_filter = ['status']
    search_fields = ['table_number__name', 'status']
    fields = ['table_number', 'status', 'description']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'table_number':
            # Get the object being edited, if any
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                # Editing an existing order
                order = Order.objects.get(pk=obj_id)
                # Include the current table plus available tables
                kwargs['queryset'] = Table.objects.filter(is_available=True, is_maintenance=True) | Table.objects.filter(pk=order.table_number.pk)
            else:
                # Creating a new order
                kwargs['queryset'] = Table.objects.filter(is_available=True, is_maintenance=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Order, OrderAdmin)