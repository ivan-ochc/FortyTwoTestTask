import json
from apps.hello.forms import ContactForm
from apps.hello.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
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


class UpdateContactTests(TestCase):
    def test_valid_form(self):
        """
        Check that form must be valid with required parameters
        """
        form_data = {
            'username': 'test',
            'email': 'test@email.com',
            'first_name': 'test_name',
            'last_name': 'test_last_name',
        }

        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

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
