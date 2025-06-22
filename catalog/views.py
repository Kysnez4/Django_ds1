# catalog
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from config.settings import CACHE_ENABLED
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

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)

        if not CACHE_ENABLED:
            return Product.objects.filter(category_id=category_id, published=True).order_by('-created_at')

        return Product.get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(Category, id=category_id)
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user = self.request.user
        context['can_edit'] = user == product.owner
        context['can_delete'] = (user == product.owner or
                                 user.has_perm('catalog.delete_product'))
        return context


@method_decorator(permission_required('catalog.can_unpublish_product', raise_exception=True), name='dispatch')
class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        product.published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect('product_detail', product_id=product_id)


@method_decorator(permission_required('catalog.delete_product', raise_exception=True), name='dispatch')
class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    pk_url_kwarg = 'product_id'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        # Разрешаем удаление владельцу или модератору
        return self.request.user == product.owner or self.request.user.has_perm('catalog.delete_product')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Товар успешно удален!')
        return response


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем пользователя в форму
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно добавлен!')
        return response


class UpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/update_product.html'
    pk_url_kwarg = 'product_id'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner  # Только владелец может редактировать

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'product_id': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно обновлен!')
        return response
