from django.urls import path

from . import views

app_name = "userauth"

urlpatterns = [
    path("sign-up/", views.UserRegisterView, name="sign-up"),
    path("sign-in/", views.loginViewTemp, name="sign-in"),
    path("sign-out/", views.LogoutView, name="sign-out"),
]
