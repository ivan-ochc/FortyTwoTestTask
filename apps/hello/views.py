import json

from apps.hello.forms import ContactForm
from apps.hello.models import WebRequest
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
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
        if request.POST:
            form = ContactForm(request.POST,
                               request.FILES,
                               instance=request.user)
            if form.is_valid():
                form.save()
            else:
                if request.is_ajax():
                    errors_dict = {}
                    if form.errors:
                        for error in form.errors:
                            e = form.errors[error]
                            errors_dict[error] = unicode(e)

                    return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            form = ContactForm(instance=request.user)
        return render(request, "contact_form.html", {'form': form})
    raise ValueError('Only authorized user has access to this view')
