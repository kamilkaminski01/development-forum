from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import Room, Topic


def login_view(request):
    context = {}
    return render(request, "base/login_register.html", context)


def home_view(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count}
    return render(request, "base/home.html", context)


def room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def create_room_view(request: HttpRequest) -> HttpResponse:
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def update_room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def delete_room_view(request: HttpRequest, pk: int) -> HttpResponse:
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)
