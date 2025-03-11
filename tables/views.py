from django.shortcuts import render, redirect, get_object_or_404

from .forms import TableForm
from .models import Table

def index(request):
    # Отображение всех столов
    tables = Table.objects.all()
    return render(request, "tables.html", {'tables': tables})


def create(request):
    # Форма создания стола
    form = TableForm()

    # Если POST
    if request.method == "POST":
        form = TableForm(request.POST)
        # Проверяем валидность формы, и сохраняем
        if form.is_valid():
            form.save()
            return redirect('tables')

    # Если не POST, то возвращаем форму
    context = {'form': form}
    return render(request, "table_form.html", context)


def update(request, table_id):
    # Обновление информации о столе.
    # Ищем стол по id
    table = get_object_or_404(Table, pk=table_id)

    # Создаем форму с его данными
    form = TableForm(request.POST or None, instance=table)
    # Отключаем возможность изменять id
    form.fields.get('id').disabled = True

    # Проверяем валидность формы, и сохраняем
    if form.is_valid():
        form.save()
        return redirect('tables')

    # Возвращаем форму
    context = {'table': table, 'form': form}
    return render(request, 'table_update.html', context)


def delete(request, table_id):
    # Удаление стола.
    # Ищем стол по id
    table = get_object_or_404(Table, pk=table_id)

    # Если POST, значит пользователь подтвердил удаление в форме
    if request.method == "POST":
        table.delete()
        return redirect('tables')

    # В противном случае отобразить форму подтверждения и информацию о столе
    context = {'table': table}
    return render(request, 'table_delete.html', context)


def delete_all(request):
    # Удаление всех столов.
    # Берем все столы
    tables = Table.objects.all()

    # Если POST, значит пользователь подтвердил удаление в форме
    if request.method == "POST":
        tables.delete()
        return redirect('tables')

    # В противном случае отобразить первые 10 столов
    context = {'tables': tables[:10], 'data_length': len(tables)}
    # Отобразить форму подтверждения и информацию о столах
    return render(request, 'table_delete_all.html', context)

def enable(request, table_id):
    # Функция включения обслуживания стола.
    # Ищем стол по id
    table = get_object_or_404(Table, pk=table_id)
    # Ставим значение
    table.is_maintenance = True
    table.save(update_fields=['is_maintenance'])

    return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу

def disable(request, table_id):
    # Функция отключения обслуживания стола.
    # Ищем стол по id
    table = get_object_or_404(Table, pk=table_id)
    # Ставим значение
    table.is_maintenance = False
    table.save(update_fields=['is_maintenance'])

    return redirect(request.META['HTTP_REFERER']) # Перенаправляем на предыдущею страницу
