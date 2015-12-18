from apps.hello.models import WebRequest
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "contact.html", {})


def requests(request):
    return render(request, "requests.html", {})


def get_requests(request):
    http_requests = WebRequest.objects.all().order_by('-id')[:10]
    data = serializers.serialize('json', http_requests)
    return JsonResponse(data, safe=False)
