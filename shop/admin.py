from django.contrib import admin
from shop.models import Category, Product, ProductImage

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)