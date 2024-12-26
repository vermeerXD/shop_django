from django.http import JsonResponse
from .models import Product, Reviews
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        user_name = request.POST.get('user_name')
        rating = request.POST.get('rating')
        content = request.POST.get('content')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Продукт не знайдено'}, status=404)

        try:
            review = Reviews.objects.create(
                user=request.user,
                product=product,
                rating=rating,
                content=content,
            )
            review.save()
            return JsonResponse({'success': True, 'message': 'Відгук успішно додано'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Некоректний метод запиту'}, status=405)