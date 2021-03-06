import json

from apps.hello import models
from django.core.management import call_command
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from apps.hello.forms import ContactForm
from apps.hello.models import User, Team
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import Template, Context
from django.test import TestCase


class ContactTests(TestCase):
    def test_create_superuser(self):
        """
        Check create_superuser function.
        """
        super_user = User.objects.create_superuser("test@email.com",
                                                   "admin",
                                                   username="admin")

        self.assertTrue(super_user.is_admin)

    def test_user_name_is_required(self):
        """
        Check that user name is required parameter.
        """
        with self.assertRaisesRegexp(ValueError,
                                     'Users must have a valid username.'):
            User.objects.create_user("test@email.com")

    def test_email_is_valid(self):
        """
        Check email validation
        """
        with self.assertRaisesRegexp(ValueError,
                                     'Users must have a valid email address.'):
            User.objects.create_user("test@", username="test")

    def test_only_unique_emails_are_accepted(self):
        """
        Check that only unique emails are accepted
        """
        with self.assertRaises(IntegrityError):
            contact = User.objects.create(email='test2@email.com')
            contact.save(force_insert=True)

    def test_home_view_user_is_authenticated(self):
        """
        Check home view with authenticated user
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        response = self.client.get(reverse('home'))
        self.assertEquals(response.context['user'].is_authenticated(), True)
        self.assertEquals(response.context['user'].username, 'test')
        self.assertEquals(response.status_code, 200)

    def test_home_view_user_is_not_authenticated(self):
        """
        Check home view with unauthenticated user
        """
        message = "Please, login to see contact information"
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        response = self.client.get(reverse('home'))
        self.assertEquals(response.context['user'].is_authenticated(), False)
        self.assertContains(response, message)


class RequestsTests(TestCase):
    def test_request_is_displayed_on_page(self):
        """
        Check that saved request is showed on page
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        response = self.client.get(reverse('requests'))
        self.assertContains(response, "requests")

    def test_last_10_requests_are_displayed_on_page(self):
        """
        Check that last 10 requests are displayed on page
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        for x in range(11):
            self.client.get(reverse('home'))
        response = self.client.get(reverse('get_requests'))
        json_string = response.content.decode('utf-8')
        requests = json.loads(json.loads(json_string))
        self.assertEquals(len(requests), 10)
        self.assertEquals(requests[9]['pk'], 2)

    def test_priority_of_request(self):
        """
        Check priority of requests
        """
        self.client.get(reverse('home'))
        request = models.WebRequest.objects.get(path='/')
        self.assertEquals(request.priority, 1)
        self.client.get(reverse('admin:index'))
        request = models.WebRequest.objects.get(path='/admin/')
        self.assertEquals(request.priority, 0)


class UpdateContactTests(TestCase):
    def test_valid_form(self):
        """
        Check that form must be valid with required parameters
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        form_data = {
            'username': 'test',
            'email': 'test@email.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'teams': 1,
        }
        response = self.client.post('/contact_form/', form_data)
        self.assertEquals(response.status_code, 200)

    def test_invalid_form(self):
        """
        Check that form must be invalid without required parameters
        """
        form_data = {
            'username': 'test',
            'email': 'test@email.com',
            'first_name': 'test_name',
        }

        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_get_edit_form_unauthorized_user(self):
        """
        Check that only authorized user has access to edit form
        """
        response = self.client.get(reverse('contact_form'))
        self.assertEquals(response.status_code, 403)

    def test_post_edit_form_unauthorized_user(self):
        """
        Check that only authorized user has access to edit form
        """
        response = self.client.post('/contact_form/',
                                    {'username': 'test',
                                     'email': 'test@email.com',
                                     'first_name': 'test_name',
                                     'last_name': 'test_last_name'})
        self.assertEquals(response.status_code, 403)


class EditTemplateTagTests(TestCase):
    def test_url_to_admin_page_is_generated_by_tag(self):
        """
        Check that tag generates url to admin edit page
        """
        user = User.objects.create_superuser("test@email.com",
                                             "admin",
                                             username="admin")
        template = Template("{% load edit_link %} {% edit_link user %}")
        rendered = template.render(Context({"user": user}))
        self.assertIn("/admin/hello/user/" + str(user.pk), rendered)


class DisplayModelsCommandTests(TestCase):
    def test_display_app_models_command(self):
        """
        Check that command returns app models name and quantity of objects
        """
        out = StringIO()
        call_command('display_models', '--app', 'hello', stdout=out)
        self.assertIn("User", out.getvalue())
        self.assertIn("WebRequest", out.getvalue())
        self.assertIn(str(models.User.objects.count()), out.getvalue())
        self.assertIn(str(models.WebRequest.objects.count()), out.getvalue())

    def test_display_project_models_command(self):
        """
        Check that command returns project models name and quantity of objects
        """
        out = StringIO()
        call_command('display_models', stdout=out)
        self.assertIn("ContentType", out.getvalue())
        self.assertIn("Permission", out.getvalue())
        self.assertIn("User", out.getvalue())
        self.assertIn("WebRequest", out.getvalue())
        self.assertIn(str(models.User.objects.count()), out.getvalue())
        self.assertIn(str(models.WebRequest.objects.count()), out.getvalue())


class SignalsTests(TestCase):
    def test_signals_are_logged(self):
        """
        Check that signals are logged
        """
        models.SignalsLog.objects.all().delete()
        User.objects.create_user("test@email.com",
                                 username="test")
        self.assertEquals(models.SignalsLog.objects.get(type='Save').type,
                          'Save')
        User.objects.filter(pk=1).update(email="test2@email.com")
        User.objects.get(pk=1).save()
        self.assertEquals(models.SignalsLog.objects.get(type='Update').type,
                          'Update')
        User.objects.filter(username="test").delete()
        self.assertEquals(models.SignalsLog.objects.get(type='Delete').type,
                          'Delete')


class TeamTests(TestCase):
    def test_get_team_form_unauthorized_user(self):
        """
        Check that only authorized user has access to team form
        """
        response = self.client.get(reverse('team_form'))
        self.assertEquals(response.status_code, 403)

    def test_post_team_form_unauthorized_user(self):
        """
        Check that only authorized user has access to team form
        """
        response = self.client.post(reverse('team_form'),
                                    kwargs={'name': 'test', 'users': 1})
        self.assertEquals(response.status_code, 403)

    def test_create_new_team(self):
        """
        Check creating of new team
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        self.client.post(reverse('team_form'), {'name': 'test', 'users': 1})
        self.assertEquals(Team.objects.get(pk=1).name, 'test')
        for user in Team.objects.get(pk=1).user.all():
            self.assertEquals(user.username, 'test')

    def test_add_team_to_user(self):
        """
        Check adding team to user
        """
        User.objects.create_user(username='test',
                                 email='test@email.com',
                                 password='test')
        self.client.login(username='test@email.com', password='test')
        self.client.post(reverse('team_form'), {'name': 'test'})
        form_data = {
            'username': 'test',
            'email': 'test@email.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
            'teams': 1,
        }
        self.client.post('/contact_form/', form_data)
        user = User.objects.get(pk=1)
        for team in user.team_set.all():
            self.assertEquals(team.name, 'test')
