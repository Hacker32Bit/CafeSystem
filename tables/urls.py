from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="tables"),
    path("create", views.create, name="create"),
    path("update/<int:table_id>", views.update, name="update"),
    path("delete/<int:table_id>", views.delete, name="delete"),
    path("delete_all", views.delete_all, name="delete-all"),
]
