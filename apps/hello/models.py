from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from smartfields import fields
from smartfields.dependencies import FileDependency
from smartfields.processors import ImageProcessor


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField(blank=True, null=True)

    email = models.EmailField(unique=True)
    jabber = models.CharField(max_length=40, unique=True, blank=True)
    skype = models.CharField(max_length=40, unique=True, blank=True)

    is_admin = models.BooleanField(default=False)

    bio = models.TextField(blank=True)
    other_contacts = models.TextField(blank=True)

    image = fields.ImageField(upload_to='img/', blank=True, dependencies=[
        FileDependency(processor=ImageProcessor(
            format='JPEG',
            scale={'max_width': 200, 'max_height': 200}))
    ])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


class WebRequest(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    method = models.CharField(max_length=50)
    uri = models.CharField(max_length=2000)
    status_code = models.IntegerField()
    get = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    priority = models.IntegerField(blank=True, null=True)


class SignalsLog(models.Model):
    type = models.CharField(max_length=7)
    payload = models.CharField(max_length=1000)


class Team(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User)
