from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse

from .forms import ProductForm
from .models import Product, Category


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 3  # Последние 3 товара

    def get_queryset(self):
        return super().get_queryset()[:3]


# Как было пусть и будет пока
class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")


class CatalogView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 6  # 6 товаров на странице


class CategoryView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/category.html'
    context_object_name = 'products'
    paginate_by = 6


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно добавлен!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при добавлении товара')
        return super().form_invalid(form)
