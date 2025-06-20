from django.urls import path
from catalog.views import (
    HomeView, ContactView, CatalogView, CategoryView, 
    ProductDetailView, AddProductView, UpdateProductView,
    DeleteProductView
)

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('category/', CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:product_id>/update/', UpdateProductView.as_view(), name='update_product'),
    path('product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete_product'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
]