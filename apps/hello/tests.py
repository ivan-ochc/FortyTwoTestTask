from apps.hello.models import User
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from wheel.signatures import assertTrue


class ContactTests(TestCase):
    def test_create_contact(self):
        contact = User.objects.create(username='test',email='test@email.com')
        assert(contact.username == 'test')
        assert(contact.email == 'test@email.com')
        contact.save()
        contact_pk = contact.pk
        assertTrue(User.objects.filter(pk=contact_pk).exists())

    def test_delete_contact(self):
        contact = User.objects.create(username='test',email='test@email.com')
        contact.save()
        contact_pk = contact.pk
        User.objects.filter(pk=contact_pk).delete()
        self.assertFalse(User.objects.filter(pk=contact_pk).exists())

    def test_only_unique_emails_are_accepted(self):
        error_occurred = False
        contact = User.objects.create(email='test@email.com')
        try:
            contact = User.objects.create(email='test@email.com')
        except IntegrityError:
            error_occurred = True

        self.assertTrue(error_occurred)

