from apps.hello.forms import ContactForm
from apps.hello.models import WebRequest, User
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


def contact_form(request):
    user = User.objects.get(pk=request.user.pk)
    if request.POST:
        form = ContactForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.jabber = form.cleaned_data['jabber']
            user.skype = form.cleaned_data['skype']
            user.is_admin = form.cleaned_data['is_admin']
            user.bio = form.cleaned_data['bio']
            user.other_contacts = form.cleaned_data['other_contacts']
            user.save()
    else:
        form = ContactForm(instance=user)
    return render(request, "contact_form.html", {'form': form})
