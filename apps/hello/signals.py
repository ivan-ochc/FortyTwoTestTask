from apps.hello import models
from apps.hello.models import SignalsLog
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save)
def model_post_save(sender, **kwargs):
    if sender in apps.get_models():
        if sender is not SignalsLog:
            save('Save', format(kwargs['instance'].__dict__))
    return


@receiver(post_delete)
def model_post_delete(sender, **kwargs):
    if sender in apps.get_models():
        if sender is not SignalsLog:
            save('Delete', format(kwargs['instance'].__dict__))
    return


def save(type, payload):
    models.SignalsLog(
        type=type,
        payload=payload,
    ).save()
