from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart, Order, OrderItem
from customers.models import Customer
from django.db import transaction
from django.utils.timezone import localtime
from django.db import connection
from django.views.decorators.http import require_GET, require_POST

def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:
            return JsonResponse({"success": False, "message": "Товару немає на складі."}, status=400)

        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        cart_item, created = Cart.objects.get_or_create(
            product=product,
            session_key=session_key,
            user=request.user if request.user.is_authenticated else None,
            defaults={'quantity': 1}
        )

        if not created:
            if cart_item.quantity + 1 > product.stock:
                return JsonResponse({"success": False, "message": "Недостатньо товару на складі."}, status=400)
            cart_item.quantity += 1
            cart_item.save()

        cart_items = Cart.objects.filter(session_key=request.session.session_key)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return JsonResponse({
            "success": True,
            "message": "Товар успішно додано в кошик.",
            "cart_items": [
                {
                    "id": item.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "total_price": item.product.price * item.quantity,
                    "product_image_url": item.product.image.url if item.product.image else None
                }
                for item in cart_items
            ],
            "total_price": total_price
        })

    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Товар не знайдено"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Помилка серверу: {str(e)}"}, status=500)

def cart_view(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    cart_items = Cart.objects.filter(
        session_key=session_key,
        user=request.user if request.user.is_authenticated else None
    )

    cart_items_with_total = [
        {
            'product': {
                'name': item.product.name,
                'price': item.product.price,
                'image_url': item.product.image.url if item.product.image else '/static/images/placeholder.jpg'
            },
            'quantity': item.quantity,
            'total': item.quantity * item.product.price,
            'id': item.id,
            'stock': item.product.stock
        }
        for item in cart_items
    ]

    total_price = sum(item['total'] for item in cart_items_with_total)
    return JsonResponse({
        'cart_items': cart_items_with_total,
        'total_price': total_price,
    })

def remove_from_cart(request, cart_id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.delete()

        return JsonResponse({'message': 'Товар успішно видалено.', 'success': True})
    return JsonResponse({'message': 'Invalid request', 'success': False}, status=400)


def change_quantity(request, cart_id, action):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=cart_id)

        if action == 'increase':
            if cart_item.quantity + 1 > cart_item.product.stock:
                return JsonResponse({'message': 'Недостатньо товару на складі', 'success': False}, status=400)
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        return JsonResponse({
            'message': 'Кількість успішно оновлена.',
            'success': True,
            'new_quantity': cart_item.quantity
        })
    return JsonResponse({'message': 'Invalid request', 'success': False}, status=400)

@login_required
def checkout(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()

    cart_items = Cart.objects.filter(
        session_key=session_key,
        user=request.user
    )

    if not cart_items:
        return redirect('cart_view')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name', customer.user.first_name)
        customer.last_name = request.POST.get('last_name', customer.user.last_name)
        customer.email = request.POST.get('email', customer.user.email)
        customer.phone_number = request.POST.get('phone_number', customer.phone_number)
        customer.country = request.POST.get('country', customer.country)
        customer.city = request.POST.get('city', customer.city)
        customer.address = request.POST.get('address', customer.address)
        customer.postal_code = request.POST.get('postal_code', customer.postal_code)
        customer.save()

        with transaction.atomic():
            order = Order.objects.create(customer=customer)

            for cart_item in cart_items:
                if cart_item.quantity > cart_item.product.stock:
                    return render(request, 'checkout.html', {
                        'cart_items': cart_items,
                        'total_price': total_price,
                        'customer': customer,
                        'error': f"Not enough stock for {cart_item.product.name}"
                    })

                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

                cart_item.delete()

            return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'customer': customer
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    if order.total_price == 0:
        order.update_total_price()

    total_price = order.total_price

    return render(request, 'order_confirmation.html', {
        'order': order,
        'total_price': total_price
    })

def cabinet(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None

    if customer:
        orders = Order.objects.filter(customer=customer)
    else:
        orders = []

    return render(request, 'cabinet.html', {'orders': orders})

@login_required
def orders_api(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    orders_data = [
        {
            'id': order.id,
            'status': order.status,
            'created_at': localtime(order.created_at).strftime('%d %B %Y, %H:%M'),
            'total_price': str(order.total_price),
            'items': [
                {
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'total_price': str(item.total_price),
                }
                for item in order.items.all()
            ]
        }
        for order in orders
    ]
    return JsonResponse({'orders': orders_data})


@login_required
@require_POST
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, customer__user=request.user)
        if order.status not in ['Завершено', 'Скасовано']:
            with transaction.atomic():
                for item in order.items.all():
                    item.product.stock += item.quantity
                    item.product.save()

                order.status = 'Скасовано'
                order.save()

            return JsonResponse({'success': True, 'message': 'Замовлення скасовано.'})
        else:
            return JsonResponse({'success': False, 'message': 'Це замовлення не можна скасувати.'}, status=400)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Замовлення не знайдено.'}, status=404)

@login_required
@require_GET
def get_customer_statistics(request):
    customer = Customer.objects.get(user=request.user)
    cust_id = customer.id

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM get_customer_statistics(%s);
        """, [cust_id])
        result = cursor.fetchone()
        if result:
            total_orders, total_spent, total_items = result
        else:
            total_orders, total_spent, total_items = 0, 0, 0

    return JsonResponse({
        "total_orders": total_orders,
        "total_spent": total_spent,
        "total_items": total_items,
    })

@require_GET
def get_total_statistics(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM get_total_statistics();
        """)
        result = cursor.fetchone()
        if result:
            total_orders, total_revenue, total_items = result
        else:
            total_orders, total_revenue, total_items = 0, 0, 0

    return JsonResponse({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_items": total_items,
    })