from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contacts/', views.contact, name='contact'),
    path('category/', views.category, name='category'),
    path('catalog/', views.catalog, name='catalog'),
]
