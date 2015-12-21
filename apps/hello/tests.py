import json

from apps.hello.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase, Client


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
        message = "Please, login to admin page to see contact information"
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
        response = self.client.get(reverse('requests'))
        self.assertContains(response, "requests")
        # self.assertContains(response, "GET")
        # self.assertContains(response, "200")

    def test_last_10_requests_are_displayed_on_page(self):
        """
        Check that last 10 requests are displayed on page
        """
        for x in range(0, 10):
            self.client.get(reverse('home'))
        response = self.client.get(reverse('get_requests'))
        json_string = response.content.decode('utf-8')
        requests = json.loads(json.loads(json_string))
        displayed_only_10_requests = True
        for request in requests:
            if request['pk'] == 0:
                displayed_only_10_requests = False

        self.assertTrue(displayed_only_10_requests)
