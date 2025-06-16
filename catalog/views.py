from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category


# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-created_at')[:3]  # Последние 3 товара
    context = {'products': products}
    return render(request, 'catalog/home.html', context=context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contact.html')

def catalog(request):
    products = Product.objects.all().order_by('-created_at')
    context = {'products': products}
    return render(request, 'catalog/catalog.html', context=context)

def category(request):
    return render(request, 'catalog/category.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context=context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(id=category_id)
            product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image
            )
            product.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении товара: {e}')

    categories = Category.objects.all()
    return render(request, 'catalog/add_product.html', {'categories': categories})

