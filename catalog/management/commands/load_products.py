import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Загружает тестовые продукты из JSON-фикстур"

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()


        with open('categories.json', 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
            for cat_data in categories_data:
                Category.objects.create(**cat_data['fields'])


        with open('products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
            for prod_data in products_data:
                # Находим категорию по id
                category_id = prod_data['fields']['category']
                category = Category.objects.get(id=category_id)
                Product.objects.create(
                    name=prod_data['fields']['name'],
                    price=prod_data['fields']['price'],
                    category=category
                )

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))