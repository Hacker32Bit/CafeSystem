from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", include("orders.urls")),
    path("products/", include("products.urls")),
    path("tables/", include("tables.urls")),
]