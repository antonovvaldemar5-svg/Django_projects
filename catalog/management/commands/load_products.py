import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстур"

    def handle(self, *args, **options):
        # Очищаем данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем фикстуры
        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))