from apps.hello.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase, Client


class ContactTests(TestCase):
    def test_create_superuser(self):
        super_user = User.objects.create_superuser("test@email.com", "admin", username="admin")
        self.assertTrue(super_user.is_admin)

    def test_user_name_is_required(self):
        with self.assertRaisesRegexp(ValueError, 'Users must have a valid username.'):
            User.objects.create_user("test@email.com")

    def test_email_is_valid(self):
        with self.assertRaisesRegexp(ValueError, 'Users must have a valid email address.'):
            User.objects.create_user("test@", username="test")

    def test_only_unique_emails_are_accepted(self):
        with self.assertRaises(IntegrityError):
            contact = User.objects.create(email='test2@email.com')
            contact.save(force_insert=True)

    def test_home_view(self):
        User.objects.create_user(username='test', email='test@email.com', password='test')
        self.client.login(username='test@email.com', password='test')
        response = self.client.get(reverse('home'))
        self.assertEquals(response.context['user'].is_authenticated(), True)
        self.assertEquals(response.context['user'].username, 'test')
        self.assertEquals(response.status_code, 200)
