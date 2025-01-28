from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            if password != confirm_password:
                messages.error(request, "Паролі не збігаються!")
                return redirect("signup")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Ця пошта вже зареєстрована!")
                return redirect("signup")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_superuser = False
            user.is_staff = False
            user.is_active = True
            user.save()

            messages.success(request, "Реєстрація успішна! Тепер увійдіть у свій акаунт.")
            return redirect("signin")

        except IntegrityError:
            messages.error(request, "Помилка під час створення акаунту. Спробуйте ще раз.")
            return redirect("signup")

    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("cabinet")
            else:
                messages.error(request, "Неправильна пошта або пароль.")
                return redirect("signin")

        except Exception as e:
            messages.error(request, f"Помилка під час входу в акаунт: {str(e)}")
            return redirect("signin")

    return render(request, "signin.html")


@login_required
def cabinet(request):
    if request.method == "POST":
        try:
            user = request.user
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()
            email = request.POST.get("email", "").strip()
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()

            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, "Ця пошта вже використовується.")
                return redirect("cabinet")

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            if password:
                user.set_password(password)
            user.save()

            messages.success(request, "Дані успішно оновлено!")
            return redirect("cabinet")

        except IntegrityError:
            messages.error(request, "Помилка під час оновлення даних. Спробуйте ще раз.")

    return render(request, "cabinet.html",{
        'is_staff': request.user.is_staff
    })