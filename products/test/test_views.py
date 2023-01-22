import json
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from products.models import Product


class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.products = {
            "Apple": Product.objects.create(name="Apple", price=10),
            "Banana": Product.objects.create(name="Banana", price=15),
        }

    def test_get_products(self):
        response = self.client.get(reverse("products:product-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_one_product(self):
        response = self.client.get(
            reverse("products:product-details", args=(self.products["Apple"].id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing_product(self):
        response = self.client.get(reverse("products:product-details", args=(100,)))
        self.assertEqual(response.status_code, 404)

    def test_create_product(self):
        data = {"name": "Pear", "price": 30}
        response = self.client.post(reverse("products:product-list"), data)
        self.assertEqual(response.status_code, 201)

    def test_create_exising_product(self):
        data = {"name": "Apple", "price": 30}
        response = self.client.post(reverse("products:product-list"), data)
        self.assertEqual(response.status_code, 400)

    def test_update_product(self):
        data = {"name": "Apple", "price": 32}
        response = self.client.put(
            reverse("products:product-details", args=(self.products["Apple"].id,)),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.products["Apple"].refresh_from_db()
        self.assertEqual(self.products["Apple"].price, data["price"])

    def test_invalid_update_product(self):
        data = {"name": "Apple", "price": 32}
        response = self.client.put(
            reverse("products:product-details", args=(self.products["Banana"].id,)),
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_product(self):
        url = reverse("products:product-details", args=(self.products["Banana"].id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        count = Product.objects.all().count()
        self.assertEqual(count, 1)
