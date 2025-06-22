from django.db import models
from django.core.cache import cache

from config import settings
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')  # Используем правильную модель

    def __str__(self):
        return self.name

    @classmethod
    def get_products_by_category(cls, category_id):
        if not settings.CACHE_ENABLED:
            return cls.objects.filter(category_id=category_id, published=True).order_by('-created_at')

        cache_key = f'products_category_{category_id}'
        products = cache.get(cache_key)
        if not products:
            products = cls.objects.filter(category_id=category_id, published=True).order_by('-created_at')
            cache.set(cache_key, products, 60 * 15)  # Кешируем на 15 минут
        return products

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]
