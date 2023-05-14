from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Topic


def topics_view(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q") if request.GET.get("q") is not None else ""
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {"topics": topics}
    return render(request, "topics.html", context)
