from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        content_type = ContentType.objects.get_for_model(Product)

        # Ищем право can_unpublish_product
        try:
            can_unpublish = Permission.objects.get(
                codename='can_unpublish_product',
                content_type=content_type,
            )
        except Permission.DoesNotExist:
            can_unpublish = Permission.objects.create(
                codename='can_unpublish_product',
                name='Может снимать продукт с публикации',
                content_type=content_type,
            )


        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        group.permissions.add(can_unpublish, delete_permission)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана/обновлена'))