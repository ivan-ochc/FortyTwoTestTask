from apps.hello.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login', 'password']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Edit your contact',
                Div(
                    'username',
                    'first_name',
                    'last_name',
                    'date_of_birth',
                    'image',
                    HTML("""{% if form.image.value %}<img id="image_preview"
                     class="img-responsive"
                     src="{{ MEDIA_URL }}{{ form.image.value }}">
                     {% endif %}""", ),

                    style="float: left; width: 40%;"
                ),
                Div(
                    'email',
                    'jabber',
                    'skype',
                    'is_admin',
                    'bio',
                    'other_contacts',
                    style="margin-left: 60%;"
                )
            )
        )
        super(ContactForm, self).__init__(*args, **kwargs)
