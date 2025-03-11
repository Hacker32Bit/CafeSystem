from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem


# Сигнал при записи нового(обновления существующего) заказа 1-го продукта в бд
@receiver(post_save, sender=OrderItem)
def update_total_price(sender, instance, **kwargs):
    # Получаем связанный order
    order = instance.order
    # Пересчитываем итоговые цены. Т.к. order изменился
    order.total_price = order.calculate_total_price()
    order.total_base_price = order.calculate_total_base_price()
    # Сохраняем
    order.save(update_fields=['total_price', 'total_base_price'])


# Сигнал при записи нового(обновления существующего) заказа в бд
@receiver(post_save, sender=Order)
def update_table_availability(sender, instance, created, **kwargs):
    # Если создан
    if created:
        # То берем его связанный Стол.
        table = instance.table_number
        if table.is_available:  # Обновляем статус свободный на False
            table.is_available = False
            table.save(update_fields=['is_available'])


# Сигнал при удалении заказа из бд
@receiver(post_delete, sender=Order)
def update_table_availability(sender, instance, **kwargs):
    # Берем его связанный Стол.
    table = instance.table_number
    if not table.is_available:   # Обновляем статус свободный на True
        table.is_available = True
        table.save(update_fields=['is_available'])