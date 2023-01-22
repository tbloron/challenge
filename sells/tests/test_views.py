from django.test import Client
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from products.models import Product
from sells.models import Order, OrderItem


class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.products = {
            "Apple": Product.objects.create(name="Apple", price=10),
            "Banana": Product.objects.create(name="Banana", price=15),
        }
        self.user = CustomUser.objects.create_user(email="client1@toto.com", password="client123")
        self.user.set_password("client123")
        self.client.login(username=self.user.email, password="client123")
        self.order = Order.objects.create(user=self.user)

    def test_get_orders(self):
        response = self.client.get(reverse("sells:order-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_one_order(self):
        url = reverse("sells:order-details", args=(self.order.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_order(self):
        url = reverse("sells:order-details", args=(100,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_item_to_order(self):
        data = {"product": self.products["Banana"].id, "quantity": 1}
        url = reverse("sells:order-details", args=(self.order.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.quantity, 1)
        self.assertEqual(self.order.amount, 15)

    def test_add_non_existing_product_to_order(self):
        data = {"product": 100, "quantity": 1}
        url = reverse("sells:order-details", args=(self.order.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_get_order_items(self):
        order_item = OrderItem(order=self.order, product=self.products["Banana"], quantity=3)
        order_item.save()
        self.order.items.add(order_item)
        order_item2 = OrderItem(order=self.order, product=self.products["Apple"], quantity=2)
        order_item2.save()
        self.order.items.add(order_item2)
        url = reverse("sells:order-details", args=(self.order.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_increment_order_item(self):
        order_item = OrderItem(order=self.order, product=self.products["Apple"], quantity=2)
        order_item.save()
        self.order.items.add(order_item)
        url = reverse("sells:item-increment", args=(self.order.id, order_item.id))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 3)

    def test_decrement_order_item(self):
        order_item = OrderItem(order=self.order, product=self.products["Apple"], quantity=2)
        order_item.save()
        self.order.items.add(order_item)
        url = reverse("sells:item-decrement", args=(self.order.id, order_item.id))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 1)

    def test_decrement_order_item_to_zero(self):
        order_item = OrderItem(order=self.order, product=self.products["Apple"], quantity=1)
        order_item.save()
        self.order.items.add(order_item)
        url = reverse("sells:item-decrement", args=(self.order.id, order_item.id))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.order.items.count(), 0)

    def test_validate_order(self):
        order_item = OrderItem(order=self.order, product=self.products["Apple"], quantity=1)
        order_item.save()
        self.order.items.add(order_item)
        url = reverse("sells:order-validate", args=(self.order.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)

    def test_get_basket(self):
        url = reverse("sells:order-basket")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)