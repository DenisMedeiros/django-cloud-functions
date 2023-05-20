import os
import django
import decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from core.models import Product, Category, Order  # noqa E402


def initialize():
    """Initialize the databse with some examples.
    """

    # Create categories.
    categories = {
        "Electronics": None,
        "Gardening": None,
        "Groceries": None,
    }
    for name in categories:
        categories[name], _ = Category.objects.get_or_create(name=name)

    # Create some products.
    products = (
        ("Television", decimal.Decimal("500.00"), categories["Electronics"]),
        ("BlueRay-Player", decimal.Decimal("200.00"), categories["Electronics"]),
        ("Smart-Speaker", decimal.Decimal("100.00"), categories["Electronics"]),
        ("Shovel", decimal.Decimal("30.00"), categories["Gardening"]),
        ("Chips", decimal.Decimal("5.00"), categories["Groceries"]),
        ("Soda", decimal.Decimal("2.00"), categories["Groceries"]),
    )

    for name, price, category in products:
        Product.objects.get_or_create(name=name, price=price, category=category)

    # Create some orders.
    order1 = Order.objects.create()
    # Add products to order.
    products = Product.objects.filter(category=categories["Groceries"])
    order1.products.add(*products)
    order1.save()

    order2 = Order.objects.create()
    # Add products to order.
    products = Product.objects.filter(
        category=categories["Electronics"]) | Product.objects.filter(category=categories["Gardening"])
    order2.products.add(*products)
    order2.save()


def main():

    initialize()


if __name__ == "__main__":
    main()
