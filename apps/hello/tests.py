from apps.hello.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase, Client


class ContactTests(TestCase):
    def test_create_contact(self):
        contact = User.objects.create(username='test', email='test@email.com')
        assert(contact.username == 'test')
        assert(contact.email == 'test@email.com')
        contact.save()
        contact_pk = contact.pk
        self.assertTrue(User.objects.filter(pk=contact_pk).exists())

    def test_delete_contact(self):
        contact = User.objects.create(username='test',email='test@email.com')
        contact.save()
        contact_pk = contact.pk
        User.objects.filter(pk=contact_pk).delete()
        self.assertFalse(User.objects.filter(pk=contact_pk).exists())

    def test_create_superuser(self):
        super_user = User.objects.create_superuser("test@email.com", "admin", username="admin")
        self.assertTrue(super_user.is_admin)

    def test_user_name_is_required(self):
        try:
            user = User.objects.create_user("test@email.com")
        except ValueError as e:
            self.assertEquals(str(e), 'Users must have a valid username.')

    def test_email_is_valid(self):
        try:
            user = User.objects.create_user("test@email", username="test")
        except ValueError as e:
            self.assertEquals(str(e), 'Users must have a valid email address.')

    def test_only_unique_emails_are_accepted(self):
        error_occurred = False
        contact = User.objects.create(email='test@email.com')
        try:
            contact = User.objects.create(email='test@email.com')
        except IntegrityError:
            error_occurred = True

        self.assertTrue(error_occurred)

    def test_home_view(self):
        contact = User.objects.create(username='test', email='test@email.com')
        contact.save()
        client = Client()
        response = client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)


