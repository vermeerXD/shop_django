# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ім\'я'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Прізвище'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        if commit:
            user.save()
        return user

class SigninForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Номер телефону'}))
    country = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Адреса доставки'}))
    postal_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Індекс'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomerForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False)
    country = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=200, required=False)
    postal_code = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Customer
        fields = ['phone_number', 'country', 'city', 'address', 'postal_code']