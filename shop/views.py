from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'index.html', {'categories': categories, 'products': products})

def products_view(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_view(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)
    return render(request, 'product.html', {'product': product})

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})