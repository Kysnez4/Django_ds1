from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Creates the 'Product Moderator' group with required permissions"

    def handle(self, *args, **options):
        # Создаем или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write("Created 'Модератор продуктов' group")
        else:
            self.stdout.write("'Модератор продуктов' group already exists")

        # Получаем разрешения
        content_type = ContentType.objects.get_for_model(Product)

        # 1. Разрешение can_unpublish_product (уже определено в модели)
        unpublish_perm = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )

        # 2. Разрешение на удаление любого продукта (стандартное delete_perm)
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Добавляем разрешения в группу
        group.permissions.add(unpublish_perm, delete_perm)
        group.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully added permissions to 'Модератор продуктов' group"
            )
        )
