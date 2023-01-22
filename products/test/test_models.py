from django.test import TestCase
from products.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Apple", price=5.50)

    def test_product_str(self):
        self.assertEqual(str(self.product), self.product.name)

    def test_product_price(self):
        self.assertEqual(self.product.price, 5.50)

    def test_product_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), f"/products/{self.product.pk}")

    def test_product_create_already_exists(self):
        with self.assertRaises(Exception):
            product = Product.objects.create(name=self.product.name, price=10)
