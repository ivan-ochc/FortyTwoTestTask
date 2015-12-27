from apps.hello import models
from apps.hello.models import User, WebRequest
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
@receiver(post_save, sender=WebRequest)
def model_post_save(sender, **kwargs):
    save('Save', format(kwargs['instance'].__dict__))


@receiver(post_delete, sender=User)
@receiver(post_delete, sender=WebRequest)
def model_post_delete(sender, **kwargs):
    save('Delete', format(kwargs['instance'].__dict__))


def save(type, payload):
    models.SignalsLog(
        type=type,
        payload=payload,
    ).save()
