from django.shortcuts import render

from tables.models import Table


def index(request):
    # Отображаем все столики с отношением заказов(order).
    tables = Table.objects.select_related('order').all()

    context = {'tables': tables}
    return render(request, "index.html", context)