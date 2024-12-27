from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from reviews.models import Reviews
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'categories': categories, 'products': products, 'page_obj': page_obj})

def products_view(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)
    reviews = Reviews.objects.filter(product=product)

    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})