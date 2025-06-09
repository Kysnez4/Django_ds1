from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'catalog/home.html')

def contact(request):
    return render(request, 'catalog/contact.html')

def catalog(request):
    return render(request, 'catalog/catalog.html')

def category(request):
    return render(request, 'catalog/category.html')