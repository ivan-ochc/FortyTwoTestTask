import json
from apps.hello.forms import ContactForm, TeamForm
from apps.hello.models import WebRequest, Team
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from setuptools.compat import unicode


def home(request):
    return render(request, "contact.html", {})


def requests(request):
    if request.user.is_authenticated():
        return render(request, "requests.html", {})
    raise PermissionDenied


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
                for team in request.user.team_set.all():
                    team.user.remove(request.user)
                for team in form.cleaned_data['teams']:
                    team.user.add(request.user)
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
            form = ContactForm(
                instance=request.user,
                initial={'teams':
                         [team.id for team in request.user.team_set.all()]})
        return render(request, "contact_form.html", {'form': form})
    raise PermissionDenied


def team_form(request):
    if request.user.is_authenticated():
        if request.POST:
            form = TeamForm(request.POST or None)
            if form.is_valid():
                form.save()
                team = Team.objects.get(name=form.cleaned_data['name'])
                for user in form.cleaned_data['users']:
                    team.user.add(user)
            else:
                if request.is_ajax():
                    errors_dict = {}
                    if form.errors:
                        for error in form.errors:
                            e = form.errors[error]
                            errors_dict[error] = unicode(e)

                    return HttpResponseBadRequest(json.dumps(errors_dict))
        else:
            form = TeamForm()
        return render(request, "team_form.html", {'form': form})
    raise PermissionDenied
