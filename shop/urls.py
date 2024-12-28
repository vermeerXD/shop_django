from django.urls import path
from . import views
from orders import views as order_views
from reviews import views as review_views

urlpatterns = [
    path('', views.index, name='home'),
    path('cabinet/', order_views.cabinet, name='cabinet'),
    path('orders/', order_views.orders_api, name='orders_api'),
    path('cancel_order/<int:order_id>/', order_views.cancel_order, name='cancel_order'),
    path('get_customer_statistics/', order_views.get_customer_statistics, name='get_customer_statistics'),
    path('get_total_statistics/', order_views.get_total_statistics, name='get_total_statistics'),
    path('checkout/', order_views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', order_views.order_confirmation, name='order_confirmation'),
    path('cart/', order_views.cart_view, name='cart'),
    path('remove-from-cart/<int:cart_id>/', order_views.remove_from_cart, name='remove_from_cart'),
    path('change-quantity/<int:cart_id>/<str:action>/', order_views.change_quantity, name='change_quantity'),
    path('submit-review/', review_views.submit_review, name='submit_review'),
    path('', views.products_view, name='products'),
    path('', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', order_views.add_to_cart, name='add_to_cart'),
    path('products/sort/<str:category_slug>/', views.sort_products, name='sort_products'),
    path('<slug:category_slug>/', views.category_view, name='category_detail'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]