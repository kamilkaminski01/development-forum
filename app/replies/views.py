from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Replies


@login_required(login_url="login")
def delete_message_view(request: HttpRequest, pk: int) -> HttpResponse:
    reply = Replies.objects.get(id=pk)
    if not request.user.is_staff and request.user != reply.user:
        return HttpResponse("You are not allowed to perform this action")
    if request.method == "POST":
        reply.delete()
        if reply.user:
            user_replies_count = reply.user.replies.filter(room=reply.room).count()
            if user_replies_count == 0:
                reply.room.participants.remove(reply.user)
        return redirect("room", pk=reply.room.id)
    return render(request, "delete.html", {"obj": reply})


def activity_view(request: HttpRequest) -> HttpResponse:
    room_messages = Replies.objects.all()[0:5]
    return render(request, "activity.html", {"room_messages": room_messages})
