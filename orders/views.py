from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from orders.forms import OrderForm, OrderItemForm
from .models import Order
from products.models import Product


# Create your views here.
def index(request):
    orders = Order.objects.all()

    context = {'orders': orders}
    return render(request, "orders.html", context)

def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    return render(request, 'order.html', {
        'order': order,
    })

def create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_forms = []

        # Create multiple item forms
        for i in range(len(request.POST.getlist('product'))):
            item_form = OrderItemForm({
                'product': request.POST.getlist('product')[i],
                'quantity': request.POST.getlist('quantity')[i],
            })
            item_forms.append(item_form)

        if order_form.is_valid() and all(f.is_valid() for f in item_forms):
            # Save order
            order = order_form.save()

            # Save order items
            for item_form in item_forms:
                item = item_form.save(commit=False)
                item.order = order
                item.save()

            # Update table availability
            order.table_number.is_available = False
            order.table_number.save(update_fields=['is_available'])

            return redirect('orders')  # Redirect to success page

    else:
        order_form = OrderForm()
        item_forms = [OrderItemForm()]

    return render(request, 'order_form.html', {
        'order_form': order_form,
        'item_forms': item_forms,
        'products': Product.objects.filter(quantity__gt=0),  # Show only available products
    })

def update(request, order_id):
    return HttpResponse("OK")

def remove(request, order_id):
    return HttpResponse("OK")

def cancel(request, order_id):
    return HttpResponse("OK")

def pay(request, order_id):
    return HttpResponse("OK")

def complete(request, order_id):
    return HttpResponse("OK")