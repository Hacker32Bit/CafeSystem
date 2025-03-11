from django.contrib import admin

from tables.models import Table
from .models import Order, OrderItem

# Убираю существующий Order из админки
admin.site.unregister(Order)

# Определяю Inline 1 заказ предмета с экстра полей для добавления товаров
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'table_number', 'status', 'total_price']
    list_filter = ['status']
    search_fields = ['table_number__name', 'status']
    fields = ['table_number', 'status', 'description']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'table_number':
            # Получаем измененный объект
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                # Если редактируемый заказ
                order = Order.objects.get(pk=obj_id)
                # Отобразить текущий стол + свободные столы
                kwargs['queryset'] = Table.objects.filter(is_available=True, is_maintenance=True) | Table.objects.filter(pk=order.table_number.pk)
            else:
                # В противном случае это новый заказ. Отображаем только свободные столы
                kwargs['queryset'] = Table.objects.filter(is_available=True, is_maintenance=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Регистрируем измененный Order, и OrderAdmin
admin.site.register(Order, OrderAdmin)