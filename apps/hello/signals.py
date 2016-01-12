from apps.hello import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save)
def model_post_save(sender, **kwargs):
    if sender is models.SignalsLog:
        return
    save('Save', format(kwargs['instance'].__dict__))


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
