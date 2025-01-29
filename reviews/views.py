import json
from django.http import JsonResponse
from .models import Product, Reviews
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


@require_POST
@csrf_protect
@login_required
def submit_review(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            rating = request.POST.get('rating')
            content = request.POST.get('content')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Продукт не знайдено'}, status=404)

            if not product_id or not rating or not content:
                return JsonResponse({'success': False, 'message': 'Всі поля мають бути заповнені'}, status=400)

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

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Некоректний формат JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Сталася помилка на сервері: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Некоректний метод запиту'}, status=405)