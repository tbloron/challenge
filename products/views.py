import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Product
from sells.models import Order, OrderItem


@csrf_exempt
def product_list(request):
    """
    Handle requests on /products endpoint

    GET
        Return an HTML page of all the products.

    POST

        Create a new Product and return its Json description.
        Payload contains the name and the unit price of the product.
        The name of a product must be unique within the scope of products

    :param request: The request
    :return: HttpResponse or JsonResponse
    """
    if request.method == "GET":
        products = Product.objects.all().order_by("name")
        context = {"product_list": products}
        return render(request, "product_list.html", context)
    elif request.method == "POST":
        try:
            name = request.POST.get("name")
            price = request.POST.get("price")
            product = Product.objects.create(name=name, price=price)
            return JsonResponse(
                {"name": name, "price": price, "pk": product.pk}, status=201
            )
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)



@csrf_exempt
def product_details(request, id):
    """
        Handle requests on /products/{id} endpoint

        GET
            Return an HTML page of the product.

        PUT

            Update a Product. Payload contains the new name and price for the product.
            The request fails when the new name is already used by another product, as
            product name must be unique.

            Return a Json description of the updated product

        DELETE

            Delete a product.

        :param request: The request
        :param id: The identifier of the Product
        :return: HttpResponse or JsonResponse
        """
    product = get_object_or_404(Product, id=id)
    if request.method == "DELETE":
        try:
            product.delete()
        except Exception as e:
            pass
        return HttpResponse(status=204)
    elif request.method == "PUT":
        body_str = request.body.decode("utf-8")
        data = json.loads(body_str)
        try:
            name = data.get("name")
            price = data.get("price")
            product.name = name
            product.price = price
            product.save()
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
        return JsonResponse(
            {"name": name, "price": price, "pk": product.pk}, status=200
        )
    elif request.method == "GET":
        try:
            context = {"product": product}
            return render(request, "product_details.html", context)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

@csrf_exempt
def product_add_to_order(request, product_id):
    """
        Handle requests on /products/{id}/add_to_order endpoint

        The product is added to the basket of the authenticated user. A basket is an order in progress
        (ordered is False). When there is no backet for the user (i.e. no order in progress), the basket
        is automatically created and the product is added to it.

        :param request: The request
        :param product_id: The identifier of the product
        :return: HttpResponse or JsonResponse
        """
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(user=user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
    else:
        order = Order.objects.create(user=user)
    order_item_qs = order.items.filter(product=product)
    if order_item_qs.exists():
        order_item = order_item_qs[0]
        order_item.quantity += 1
        order_item.amount += product.price
        order_item.save()
    else:
        order_item = OrderItem(order=order, product=product, quantity=1, amount=product.price)
        order_item.save()
        order.items.add(order_item)
    return JsonResponse({"product": product.name, "order": order.pk}, status=201)
