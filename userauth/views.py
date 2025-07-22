from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .models import Profile, User


def UserRegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in ")
        return redirect("hotel:index")

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        phone = form.cleaned_data.get("phone")
        password = form.cleaned_data.get("password1")

        user = authenticate(request, email=email, password=password)
        login(request, user)

        messages.success(
            request, f"Hey {full_name} .Your account has been created succefully"
        )

        profile = Profile.objects.get(user=user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()
        return redirect("hotel:index")

    context = {"form": form}
    return render(request, "userauth/sign_up.html", context)


def loginViewTemp(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in ")
        return redirect("hotel:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_query = User.objects.get(email=email)
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                login(request, user_auth)
                messages.success(request, "You are logged in")
                next_url = request.GET.get("next", "hotel:index")
                return redirect("hotel:index")
            else:
                messages.warning(request, "username or password does not exist")
                return redirect("userauth:sign-up")
        except:
            messages.warning(request, "username or password does not exist")
            return redirect("userauth:sign-up")
    return render(request, "userauth/sign-in.html")


def LogoutView(request):
    logout(request)
    messages.success(request, "you have been logged out ")
    return redirect("userauth:sign-in")
