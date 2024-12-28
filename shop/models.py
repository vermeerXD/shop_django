from django.db import models
import os

# Create your models here.
class Category(models.Model):
    """
    Model for categories
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL категорії")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def get_filters(self):
        if self.name.lower() == "смартфони":
            return [
                {"name"}
            ]

    def __str__(self):
        return self.name

def product_image_path(instance, filename):
    return os.path.join('products', filename)

class Product(models.Model):
    """
    Model for products
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія"
    )
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва продукту")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL продукту")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    stock = models.PositiveIntegerField(verbose_name="Кількість на складі")
    available = models.BooleanField(default=True, verbose_name="Доступність")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True, verbose_name="Картинка")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"
        ordering = ["name"]

    @property
    def reviews(self):
        return self.reviews_set.all()

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
