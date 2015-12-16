from apps.hello.models import User
from django.contrib.auth import get_user
from django.shortcuts import render


def home(request):
    context = {}
    if request.user.is_authenticated():
        queryset = User.objects.get(pk=get_user(request).pk)
        context = {
            "contacts": queryset
        }
    return render(request, "base.html", context)
