from apps.hello.forms import ContactForm
from apps.hello.models import User
from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    form = ContactForm

admin.site.register(User, ContactAdmin)
