from django.test import TestCase

from users.models import CustomUser
from sells.models import Order, OrderItem
from products.models import Product


class SellsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="client@toto.com", password="client123")
        self.order = Order.objects.create(user=self.user)
        self.product = {
            "Apple": Product.objects.create(name="Apple", price=10.5),
            "Banana": Product.objects.create(name="Banana", price=15),
        }

    def test_order_user(self):
        self.assertEqual(self.order.user.username, self.user.username)

    def test_order_not_ordered(self):
        self.assertEqual(self.order.ordered, False)
        self.assertEqual(self.order.ordered_at, None)

    def test_order_no_items(self):
        self.assertEquals(self.order.items.all().count(), 0)

    def test_order_add_items(self):
        order_item = OrderItem.objects.create(product=self.product["Apple"], quantity=1)
        order_item.save()
        self.order.items.add(order_item)
        self.assertEqual(self.order.quantity, 1)
        self.assertEqual(self.order.amount, self.product["Apple"].price)
        order_item.quantity += 1
        order_item.save()
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.amount, 21)

    def test_order_delete_items(self):
        order_item = OrderItem.objects.create(product=self.product["Apple"], quantity=1,)
        order_item.save()
        self.order.items.add(order_item)
        self.assertEqual(self.order.items.count(), 1)
        order_item.delete()
        self.assertEqual(self.order.items.count(), 0)
