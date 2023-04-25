from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from topics.models import Topic

from .forms import CustomUserCreationForm, UserForm
from .models import User


def user_profile_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)  # type: ignore
    rooms = user.room_host.all()
    room_messages = user.replies.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "profile.html", context)


@login_required(login_url="login")
def update_user(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", user.id)
    return render(request, "users/update-user.html", {"form": form})


def register_view(request: HttpRequest) -> HttpResponse:
    form: CustomUserCreationForm = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, "users/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        if email := request.POST.get("email"):
            email = email.lower()
            password = request.POST.get("password")
            user_exists = User.objects.filter(email=email).exists()  # type: ignore
            if user_exists:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(request, "Incorrect email or password")
            else:
                messages.error(request, "User doesn't exist")
    return render(request, "users/login.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
