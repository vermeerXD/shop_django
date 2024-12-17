from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('', views.products_view, name='products'),
    path('', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.category_view, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]