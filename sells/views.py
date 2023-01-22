from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Order, OrderItem
from products.models import Product


@csrf_exempt
def order_list(request):
    """
    Handle requests on /sells endpoint

    GET
        Return an HTML page of all the sells.

    :param request: The request
    :return: HttpResponse
    """
    if request.method == "GET":
        orders = Order.objects.filter(ordered=True).order_by('-ordered_at')
        user = request.user
        if not user.is_superuser and not user.is_staff:
            orders = orders.filter(user=user)
        context = {"order_list": orders}
        return render(request, "order_list.html", context)


@csrf_exempt
def order_basket(request):
    """
    Handle requests on /sells/basket endpoint

    GET
        Return the identifier of the basket of the authenticated user. Only customers (i.e. non admin users)
        have a basket as an order in progress. When no basket exists for the user, it is
        automatically created.

    :param request: The request
    :return: JsonResponse
    """
    user = request.user
    if user.is_superuser or user.is_staff:
        return JsonResponse({"message": "Forbidden access"}, status=403)
    try:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
        else:
            order = Order.objects.create(user=user)
        return JsonResponse({"pk": order.pk}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


def has_order_permission(user, order):
    return order.user == user or user.is_superuser or user.is_staff


@csrf_exempt
def order_details(request, id):
    """
    Handle requests on /sells/{id} endpoint

    GET
        Return an HTML page of an order (validated or in progress).

    POST
        Add a product and quantity to the order. Payload contains product (identifier) and quantity (integer)
        to be added to the order. If the order already contains item of the product, its quantity is incremented
        by the given quantity.
        Return a Json description of the order.

    :param request: The request
    :param id: The identifier of the order
    :return: JsonResponse
    """
    order = get_object_or_404(Order, id=id)
    if not has_order_permission(request.user, order):
        return JsonResponse({"message": "Forbidden access"}, status=403)
    if request.method == "GET":
        context = {"order": order, "order_items": order.items.all().order_by("product__name")}
        return render(request, "order_details.html", context)
    elif request.method == "POST":
        try:
            product_id = request.POST.get("product")
            quantity = request.POST.get("quantity")
            product = Product.objects.get(id=product_id)
            order_item = order.items.filter(product=product).first()
            if order_item is not None:
                order_item.quantity += quantity
                order_item.save()
            else:
                data = {
                    "order": order,
                    "product": product,
                    "quantity": quantity,
                }
                order_item = OrderItem.objects.create(**data)
                order.items.add(order_item)
            return JsonResponse(
                {
                    "pk": order_item.pk,
                    "order": order.pk,
                    "quantity": order_item.quantity,
                    "amount": order_item.amount,
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)


@csrf_exempt
def item_details(request, order_id, id):
    """
    Handle requests on /sells/{order_id}/items/{id} endpoint

    DELETE
        Remove an item from the order.

    :param request: The request
    :param order_id: The identifier of the order
    :param id: The identifier of the item to be removed
    :return: HttpResponse
    """
    order_item = OrderItem.objects.get(id=id, order_id=order_id)
    if not has_order_permission(request.user, order_item.order):
        return JsonResponse({"message": "Forbidden access"}, status=403)
    if request.method == "DELETE":
        order_item.delete()
        return HttpResponse(status=204)


@csrf_exempt
def item_increment(request, order_id, id):
    """
    Handle requests on /sells/{order_id}/items/{id}/increment endpoint

    POST
        Increment the quantity of an item of the order.

    :param request: The request
    :param order_id: The identifier of the order
    :param id: The identifier of the item to be removed
    :return: HttpResponse
    """
    order_item = OrderItem.objects.get(id=id)
    if not has_order_permission(request.user, order_item.order):
        return JsonResponse({"message": "Forbidden access"}, status=403)
    order_item.quantity += 1
    order_item.amount += order_item.product.price
    order_item.save()
    return HttpResponse(status=204)


@csrf_exempt
def item_decrement(request, order_id, id):
    """
    Handle requests on /sells/{order_id}/items/{id}/decrement endpoint

    POST
        Decrement the quantity of an item of the order. When the quantity drops to 0,
        the item is removed from the order

    :param request: The request
    :param order_id: The identifier of the order
    :param id: The identifier of the item to be removed
    :return: HttpResponse
    """
    order_item = OrderItem.objects.get(id=id)
    if not has_order_permission(request.user, order_item.order):
        return JsonResponse({"message": "Forbidden access"}, status=403)
    order_item.quantity -= 1
    order_item.amount -= order_item.product.price
    if order_item.quantity <= 0:
        order_item.delete()
    else:
        order_item.save()
    return HttpResponse(status=204)


@csrf_exempt
def order_validate(request, id):
    """
    Handle requests on /sells/{order_id}/validate endpoint

    POST
        Validate an order. The order cannot be updated any longer. Only customers can validate
        their orders.

    :param request: The request
    :param id: The identifier of the order to validate
    :return: HttpResponse
    """
    order = Order.objects.get(id=id)
    if not has_order_permission(request.user, order):
        return JsonResponse({"message": "Forbidden access"}, status=403)
    order.ordered = True
    order.ordered_at = timezone.now()
    order.save()
    return HttpResponse(status=204)
