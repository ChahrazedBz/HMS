from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": " Enter your Full name "})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": " Choose a username"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": " Enter your email"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": " Enter your phone number"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": " Create a password "})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": " Confirm your password"})
    )

    class Meta:
        model = User
        fields = ["full_name", "username", "email", "phone", "password1", "password2"]
