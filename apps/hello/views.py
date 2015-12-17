from apps.hello.models import User
from django.contrib.auth import get_user
from django.shortcuts import render


def home(request):
    return render(request, "base.html", {})



