from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product-details", kwargs={"id": self.id})
