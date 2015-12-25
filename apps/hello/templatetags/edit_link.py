from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(name="edit_link")
def edit_link(obj):
    if not obj:
        raise template.TemplateSyntaxError("Such object doesn't exist")
    return reverse('admin:' + obj._meta.app_label + '_' +
                   obj.__class__.__name__.lower() +
                   '_change', args=(obj.pk,))
