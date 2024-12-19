from django.urls import path
from . import views
from orders import views as order_views

urlpatterns = [
    path('', views.index, name='home'),
    path('cabinet/', order_views.cabinet, name='cabinet'),
    path('orders/', order_views.orders_api, name='orders_api'),
    path('checkout/', order_views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', order_views.order_confirmation, name='order_confirmation'),
    path('cart/', order_views.cart_view, name='cart'),
    path('remove-from-cart/<int:cart_id>/', order_views.remove_from_cart, name='remove_from_cart'),
    path('change-quantity/<int:cart_id>/<str:action>/', order_views.change_quantity, name='change_quantity'),
    path('', views.products_view, name='products'),
    path('', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name='add_to_cart'),
    path('<slug:category_slug>/', views.category_view, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]