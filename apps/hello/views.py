import json

from apps.hello.forms import ContactForm
from apps.hello.models import WebRequest, User
from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from setuptools.compat import unicode


def home(request):
    return render(request, "contact.html", {})


def requests(request):
    if request.user.is_authenticated():
        return render(request, "requests.html", {})
    raise ValueError('Only authorized user has access to this view')


def get_requests(request):
    http_requests = WebRequest.objects.all().order_by('-id')[:10]
    data = serializers.serialize('json', http_requests)
    return JsonResponse(data, safe=False)


def contact_form(request):
    if request.user.is_authenticated():
        user = User.objects.get(pk=request.user.pk)
        if request.POST:
            form = ContactForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()

                if request.is_ajax():
                    if getattr(settings, 'DEBUG', False):
                        import time
                        time.sleep(2)

            else:
                if request.is_ajax():
                    errors_dict = {}
                    if form.errors:
                        for error in form.errors:
                            e = form.errors[error]
                            errors_dict[error] = unicode(e)

                    return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            form = ContactForm(instance=user)
        return render(request, "contact_form.html", {'form': form})
    raise ValueError('Only authorized user has access to this view')


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login_inactive.html', {})
    else:
        return render(request, 'login_none.html', {})
