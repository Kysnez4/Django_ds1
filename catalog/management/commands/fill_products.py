from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = "Fill the database with test products (deletes old data first)"

    def handle(self, *args, **options):
        # Удаляем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Old data deleted.")

        # Создаем категории
        electronics = Category.objects.create(
            name="Электроника",
            description="Гаджеты и устройства"
        )
        clothing = Category.objects.create(
            name="Одежда",
            description="Модная одежда"
        )
        self.stdout.write("Categories created.")

        # Создаем продукты
        products = [
            {
                "name": "Смартфон",
                "description": "Мощный смартфон",
                "price": 599.99,
                "category": electronics
            },
            {
                "name": "Ноутбук",
                "description": "Игровой ноутбук",
                "price": 1299.99,
                "category": electronics
            },
            {
                "name": "Футболка",
                "description": "Хлопковая футболка",
                "price": 19.99,
                "category": clothing
            }
        ]

        for product_data in products:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS("Successfully filled the database with test products!"))
