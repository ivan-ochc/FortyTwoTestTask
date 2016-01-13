from apps.hello import models
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save)
def model_post_save(sender, created, **kwargs):
    action = 'Save' if created else 'Update'
    if sender in apps.get_models():
        if sender is models.SignalsLog:
            return
        save(action, format(kwargs['instance'].__dict__))


@receiver(post_delete)
def model_post_delete(sender, **kwargs):
    if sender is models.SignalsLog:
        return
    save('Delete', format(kwargs['instance'].__dict__))


def save(type, payload):
    models.SignalsLog(
        type=type,
        payload=payload,
    ).save()
