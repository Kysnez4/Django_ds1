# catalog
from django.core.cache import cache
from django.conf import settings

from catalog.models import Product


class ProductService:
    @staticmethod
    def get_products_by_category(category_id):
        """
        Возвращает список продуктов в указанной категории с кешированием
        """
        if not settings.CACHE_ENABLED:
            return Product.objects.filter(
                category_id=category_id,
                published=True
            ).order_by('-created_at')

        cache_key = f'products_category_{category_id}'
        products = cache.get(cache_key)

        if not products:
            products = list(Product.objects.filter(
                category_id=category_id,
                published=True
            ).order_by('-created_at'))
            cache.set(cache_key, products, 60 * 15)

        return products

    @staticmethod
    def invalidate_category_cache(category_id):
        """
        Сбрасывает кеш для указанной категории
        """
        cache.delete(f'products_category_{category_id}')