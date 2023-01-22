from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("<int:id>", views.product_details, name="product-details"),
    path("<int:product_id>/add_to_order", views.product_add_to_order, name="product-add-to-order",),
]
