from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from reviews.models import Reviews
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from product.models import Smartphone, Case, ScreenProtector, PowerBank, CableAndAdapter, Charger


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
    brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by')
    order = request.GET.get('order', 'asc')

    if brand:
        products = products.filter(
            Q(smartphone__brand=brand) |
            Q(case__brand=brand) |
            Q(screen_protector__brand=brand) |
            Q(power_bank__brand=brand) |
            Q(cable_adapter__brand=brand) |
            Q(charger__brand=brand)
        )

    if sort_by:
        sort_order = '' if order == 'asc' else '-'
        products = products.order_by(f"{sort_order}{sort_by}")

    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'brands': get_unique_brands(category),
    })

def get_unique_brands(category):
    brands = set()
    if category.id == 5:
        brands.update(Smartphone.objects.filter(product__category=category).values_list('brand', flat=True))
    elif category.id == 2:
        brands.update(Case.objects.filter(product__category=category).values_list('brand', flat=True))
    elif category.id == 3:
        brands.update(ScreenProtector.objects.filter(product__category=category).values_list('brand', flat=True))
    elif category.id == 4:
        brands.update(PowerBank.objects.filter(product__category=category).values_list('brand', flat=True))
    elif category.id == 6:
        brands.update(CableAndAdapter.objects.filter(product__category=category).values_list('brand', flat=True))
    elif category.id == 7:
        brands.update(Charger.objects.filter(product__category=category).values_list('brand', flat=True))
    return sorted(brands)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)
    reviews = Reviews.objects.filter(product=product)

    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})


def sort_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    sort_by = request.GET.get('sort_by', 'price')
    order = request.GET.get('order', 'asc')
    brand_id = request.GET.get('brand')

    products = Product.objects.filter(category=category)

    if brand_id:
        if category.id == 5:
            products = products.filter(smartphone__brand=brand_id)
        elif category.id == 2:
            products = products.filter(case__brand=brand_id)
        elif category.id == 3:
            products = products.filter(screen_protector__brand=brand_id)
        elif category.id == 4:
            products = products.filter(power_bank__brand=brand_id)
        elif category.id == 6:
            products = products.filter(cable_adapter__brand=brand_id)
        elif category.id == 7:
            products = products.filter(charger__brand=brand_id)

    if order == 'desc':
        sort_by = f'-{sort_by}'

    products = products.order_by(sort_by).distinct()

    data = {
        'products': [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image.url if product.image else None,
                'slug': product.slug,
                'category_slug': product.category.slug,
            }
            for product in products
        ]
    }
    return JsonResponse(data)