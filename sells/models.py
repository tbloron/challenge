from django.db import models
from django.urls import reverse
from django.conf import settings

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return f"Order-{self.pk}"

    def get_absolute_url(self):
        return reverse("sells:order-details", kwargs={"id": self.id})

    @property
    def quantity(self):
        quantity = 0
        for item in self.items.all():
            quantity += item.quantity
        return quantity

    @property
    def amount(self):
        amount = 0
        for item in self.items.all():
            amount += float(item.amount)
        return amount


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.amount = int(self.quantity) * float(self.product.price)
        super().save(*args, **kwargs)
