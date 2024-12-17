from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignupForm, SigninForm, ProfileForm, CustomerForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

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

    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("cabinet")
        else:
            messages.error(request, "Неправильна пошта або пароль.")
            return redirect("signin")

    return render(request, "signin.html")


@login_required
def cabinet(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, "Дані успішно оновлено!")
        return redirect("cabinet")

    return render(request, "cabinet.html")