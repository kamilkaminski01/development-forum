from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from replies.models import Replies
from topics.models import Topic

from .forms import RoomForm
from .models import Room


def home_view(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    rooms_count = rooms.count()
    room_messages = Replies.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, "home.html", context)


def room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    room_messages = room.replies.all()
    participants = room.participants.all()
    if request.method == "POST":
        if body := request.POST.get("body"):
            if request.user.is_authenticated:
                Replies.objects.create(user=request.user, room=room, body=body)
                room.participants.add(request.user)
                return redirect("room", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "rooms/room.html", context)


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
    return render(request, "rooms/room_form.html", context)


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
    return render(request, "rooms/room_form.html", context)


@login_required(login_url="login")
def delete_room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "delete.html", context)
