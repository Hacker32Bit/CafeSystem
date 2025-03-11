from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductForm
from .models import Product

def index(request):
    # Отображение всех продуктов
    products = Product.objects.all()
    return render(request, "products.html", {'products': products})


def create(request):
    # Форма создания продукта
    form = ProductForm()

    # Если POST
    if request.method == "POST":
        form = ProductForm(request.POST)
        # Проверяем валидность формы и сохраняем в бд
        if form.is_valid():
            form.save()
            return redirect('products')

    # Если не POST, то отображаем форму
    context = {'form': form}
    return render(request, "product_form.html", context)


def update(request, product_id):
    # Форма изменения продукта.
    # Получаем продукт по id
    product = get_object_or_404(Product, pk=product_id)

    # Создаем заполненную форму
    form = ProductForm(request.POST or None, instance=product)

    # Проверяем форму и сохраняем
    if form.is_valid():
        form.save()
        return redirect('products')

    # Если не валидна. То отображаем форму
    context = {'product': product, 'form': form}
    return render(request, 'product_update.html', context)


def delete(request, product_id):
    # Удаление. Ищем продукт по id
    product = get_object_or_404(Product, pk=product_id)

    # Если POST, значит пользователь подтвердил, и удаляем
    if request.method == "POST":
        product.delete()
        return redirect('products')

    # В противном случае отображаем страницу с подтверждением
    context = {'product': product}
    return render(request, 'product_delete.html', context)


def delete_all(request):
    # Удаление. Ищем все продукты
    products = Product.objects.all()

    # Если POST, значит пользователь подтвердил, и удаляем
    if request.method == "POST":
        products.delete()
        return redirect('products')

    # В контексте отображаем первые 10
    context = {'products': products[:10], 'data_length': len(products)}
    # В противном случае отображаем страницу с подтверждением
    return render(request, 'product_delete_all.html', context)
