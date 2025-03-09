from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm
from .models import Product

def index(request):
    products = Product.objects.all()
    return render(request, "products.html", {'products': products})


def create(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, "product_form.html", context)


def update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('products')

    context = {'product': product, 'form': form}
    return render(request, 'product_update.html', context)


def delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    if request.method == "POST":
        product.delete()
        return redirect('products')

    return render(request, 'product_delete.html', context)


def delete_all(request):
    products = Product.objects.all()
    context = {'products': products[:10], 'data_length': len(products)}
    if request.method == "POST":
        products.delete()
        return redirect('products')

    return render(request, 'product_delete_all.html', context)
