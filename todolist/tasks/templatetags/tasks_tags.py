from django import template

from tasks.forms import UpdateForm

register = template.Library()


@register.simple_tag
def get_update_form_for(instance):
    return UpdateForm(model_instance=instance)
