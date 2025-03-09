from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="tables"),
    path("create", views.create, name="table-create"),
    path("update/<int:table_id>", views.update, name="table-update"),
    path("delete/<int:table_id>", views.delete, name="table-delete"),
    path("delete_all", views.delete_all, name="table-delete-all"),
]
