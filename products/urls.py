from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="products"),
    path("create", views.create, name="product-create"),
    path("update/<int:product_id>", views.update, name="product-update"),
    path("delete/<int:product_id>", views.delete, name="product-delete"),
    path("delete_all", views.delete_all, name="product-delete-all"),
]
