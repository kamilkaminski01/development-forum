from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Replies


@login_required(login_url="login")
def delete_message_view(request: HttpRequest, pk: int) -> HttpResponse:
    message = Replies.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "delete.html", {"obj": message})


def activity_view(request: HttpRequest) -> HttpResponse:
    room_messages = Replies.objects.all()[0:5]
    return render(request, "activity.html", {"room_messages": room_messages})
