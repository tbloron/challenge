from django.urls import path

from . import views

app_name = "sells"


urlpatterns = [
    path("", views.order_list, name="order-list"),
    path("<int:id>", views.order_details, name="order-details"),
    path("basket/", views.order_basket, name="order-basket"),
    path("<int:id>/validate", views.order_validate, name="order-validate"),
    path("<int:order_id>/items/<int:id>", views.item_details, name="item-details"),
    path("<int:order_id>/items/<int:id>/increment", views.item_increment, name="item-increment"),
    path("<int:order_id>/items/<int:id>/decrement", views.item_decrement, name="item-decrement"),
]
