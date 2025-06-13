from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contact, name='contact'),
    path('category/', views.category, name='category'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
]