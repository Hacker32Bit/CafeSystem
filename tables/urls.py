from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="tables"),
    path("create", views.create, name="table-create"),
    path("update/<int:table_id>", views.update, name="table-update"),
    path("delete/<int:table_id>", views.delete, name="table-delete"),
    path("enable/<int:table_id>", views.enable, name="table-enable"),
    path("disable/<int:table_id>", views.disable, name="table-disable"),
    path("delete_all", views.delete_all, name="table-delete-all"),
]
