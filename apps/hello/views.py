from apps.hello.models import User
from django.shortcuts import render


def home(request):
    queryset = User.objects.get(pk=1)
    context = {
        "contacts": queryset
    }
    print(queryset)
    return render(request, "base.html", context)
