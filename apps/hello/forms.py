from apps.hello.models import User
from django import forms


class ContactForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login', 'password']
