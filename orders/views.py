from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from orders.forms import OrderForm, OrderItemForm
from .models import Order
from products.models import Product


def index(request):
    # Отображаем список всех заказов
    orders = Order.objects.all()

    context = {'orders': orders}
    return render(request, "orders.html", context)

def order(request, order_id):
    # Отображаем определенный заказ по order_id
    order = get_object_or_404(Order, pk=order_id)

    return render(request, 'order.html', {
        'order': order,
    })

def create(request):
    # Cоздание заказа.
    # Если пост. Значит отправка формы
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_forms = []

        # Создаем список заказа 1-го продукта(OrderItem) из полученной формы.
        for i in range(len(request.POST.getlist('product'))):
            item_form = OrderItemForm({
                'product': request.POST.getlist('product')[i],
                'quantity': request.POST.getlist('quantity')[i],
            })
            item_forms.append(item_form)

        if order_form.is_valid() and all(f.is_valid() for f in item_forms):
            # Если все валидно(т.е. форма без ошибок), то сохраняем форму
            order = order_form.save()

            # Сохраняем все items-ы(продукты)
            for item_form in item_forms:
                item = item_form.save(commit=False)
                item.order = order
                item.save()

            # Обновляем статус стола на занят(False)
            order.table_number.is_available = False
            order.table_number.save(update_fields=['is_available'])

            return redirect('orders')  # Перенаправляем на список заказов

    # Если не POST, то создаем форму
    else:
        order_form = OrderForm()
        item_forms = [OrderItemForm()]

    # Рендер страницы передав форму заказа и выбора продуктов
    return render(request, 'order_form.html', {
        'order_form': order_form,
        'item_forms': item_forms,
        'products': Product.objects.filter(quantity__gt=0),  # Отображаем только те продукты у которых есть кол-во
    })

def update(request, order_id):
    # TODO
    return HttpResponse("OK")

def remove(request, order_id):
    # Ищем заказ по order_id
    order = get_object_or_404(Order, pk=order_id)
    context = {'order': order}
    # Если POST значит стоит галочка подтверждения и нажата кнопка удалить
    if request.method == "POST":
        order.delete()
        return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу

    # В противном случае(если не POST) отображаем страницу о заказе и подтверждении удалении
    return render(request, 'order_delete.html', context)

def remove_all(request):
    # Берем все заказы
    orders = Order.objects.all()

    # Если POST значит стоит галочка подтверждения и нажата кнопка удалить
    if request.method == "POST":
        orders.delete()
        return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу

    # В противном случае(если не POST) в контексте отображаем первые 10 заказов
    context = {'orders': orders[:10], 'data_length': len(orders)}
    return render(request, 'order_delete_all.html', context)

def cancel(request, order_id):
    # TODO
    return HttpResponse("OK")

def cancel_all(request):
    # TODO
    return HttpResponse("OK")

def pay(request, order_id):
    # Нажата кнопка оплатить.
    # Ищем заказ с этим id
    order = get_object_or_404(Order, pk=order_id)
    # Ставим статус PAID
    order.status = "PAID"
    order.save(update_fields=['status'])

    return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу


# Ниже 2 функции complete и pending аналогичны pay
def complete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = "COMPLETED"
    order.save(update_fields=['status'])

    return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу

def pending(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = "PENDING"
    order.save(update_fields=['status'])

    return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу