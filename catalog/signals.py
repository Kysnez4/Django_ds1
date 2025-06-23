# catalog
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .services.product_service import ProductService

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Сбрасывает кеш при изменении продукта
    """
    ProductService.invalidate_category_cache(instance.category_id)