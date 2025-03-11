from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="orders"),
    path("<int:order_id>", views.order, name="order"),
    path("create", views.create, name="order-create"),
    path("update/<int:order_id>", views.update, name="order-update"),
    path("remove/<int:order_id>", views.remove, name="order-remove"),
    path("remove_all", views.remove_all, name="order-remove-all"),
    path("cancel/<int:order_id>", views.cancel, name="order-cancel"),
    path("cancel_all/", views.cancel_all, name="order-cancel-all"),
    path("complete/<int:order_id>", views.complete, name="order-complete"),
    path("pay/<int:order_id>", views.pay, name="order-pay"),
    path("pending/<int:order_id>", views.pending, name="order-pending"),
]
