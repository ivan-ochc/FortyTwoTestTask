from apps.hello.models import User, WebRequest
from django.contrib.auth import get_user
from django.shortcuts import render


def home(request):
    return render(request, "base.html", {})


def requests(request):
    http_requests = WebRequest.objects.all().order_by('-id')[:10]
    context = {
        "http_requests": http_requests
    }
    return render(request, "requests.html", context)
