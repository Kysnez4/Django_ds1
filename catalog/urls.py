from django.urls import path
from .views import (
    HomeView,
    ContactView,
    CatalogView,
    CategoryView,
    ProductDetailView,
    AddProductView
)

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('category/', CategoryView.as_view(), name='category'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
]