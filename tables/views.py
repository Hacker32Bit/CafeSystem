from django.forms import Textarea
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TableForm
from .models import Table

def index(request):
    tables = Table.objects.all()
    return render(request, "tables.html", {'tables': tables})


def create(request):
    form = TableForm()

    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables')

    context = {'form': form}
    return render(request, "form.html", context)


def update(request, table_id):
    table = get_object_or_404(Table, pk=table_id)

    form = TableForm(request.POST or None, instance=table)
    form.fields.get('id').disabled = True

    if form.is_valid():
        form.save()
        return redirect('tables')

    context = {'table': table, 'form': form}
    return render(request, 'update.html', context)


def delete(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    context = {'table': table}
    if request.method == "POST":
        table.delete()
        return redirect('tables')

    return render(request, 'delete.html', context)


def delete_all(request):
    tables = Table.objects.all()
    context = {'tables': tables[:10], 'data_length': len(tables)}
    if request.method == "POST":
        tables.delete()
        return redirect('tables')

    return render(request, 'delete_all.html', context)
