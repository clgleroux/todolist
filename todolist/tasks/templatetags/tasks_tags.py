from django import template

from tasks.forms import (
    UpdateForm, EditForm)

register = template.Library()


@register.simple_tag
def get_update_form_for(instance):
    return UpdateForm(model_instance=instance)


@register.simple_tag
def get_edit_form_for(instance):
    return EditForm(model_instance=instance)
