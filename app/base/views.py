from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm, UserForm
from .models import Message, Room, Topic


def register_view(request: HttpRequest) -> HttpResponse:
    form: UserCreationForm = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, "base/login_register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        if username := request.POST.get("username"):
            username = username.lower()
            password = request.POST.get("password")
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(request, "Incorrect username or password")
            else:
                messages.error(request, "User doesn't exist")
    return render(request, "base/login_register.html", {"page": page})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


def home_view(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        if body := request.POST.get("body"):
            if request.user.is_authenticated:
                Message.objects.create(user=request.user, room=room, body=body)
                room.participants.add(request.user)
                return redirect("room", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def user_profile_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def create_room_view(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        user = request.user
        room_name = request.POST.get("name")
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        if user.is_authenticated and room_name:
            host = user if isinstance(user, User) else None
            Room.objects.create(
                host=host,
                topic=topic,
                name=room_name,
                description=request.POST.get("description"),
            )
            return redirect("home")
    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def update_room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        if room_name := request.POST.get("name"):
            room.name = room_name
            room.topic = topic
            room.description = request.POST.get("description")
            room.save()
            return redirect("home")
    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def delete_room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def delete_message_view(request: HttpRequest, pk: int) -> HttpResponse:
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": message})


@login_required(login_url="login")
def update_user(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user-profile", user.id)
    return render(request, "base/update-user.html", {"form": form})


def topics_view(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activity_view(request: HttpRequest) -> HttpResponse:
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})
