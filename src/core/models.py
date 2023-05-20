import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "name": self.name
        }


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category.name
        }


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.id)

    def as_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "products": [product.name for product in self.products]
        }
