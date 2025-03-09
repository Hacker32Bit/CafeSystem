from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(post_save, sender=OrderItem)
def update_total_price(sender, instance, **kwargs):
    # Get the related order
    order = instance.order
    # Recalculate total price
    order.total_price = order.calculate_total_price()
    order.total_base_price = order.calculate_total_base_price()
    # Save the updated price
    order.save(update_fields=['total_price', 'total_base_price'])


@receiver(post_save, sender=Order)
def update_table_availability(sender, instance, created, **kwargs):
    if created:
        # Set the related table's is_available to False only when a new order is created
        table = instance.table_number
        if table.is_available:  # Update only if currently available
            table.is_available = False
            table.save(update_fields=['is_available'])