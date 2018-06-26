from django import forms

import unicodedata

from django.forms import ModelForm
from django.forms.fields import CharField
from django.forms.fields import TypedChoiceField
from tasks.models import Task
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm as UserCreationFrom_


class CreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']
        labels = {
            "description": _("Description"),
        }


class DescriptionTask(forms.Textarea):
    template_name = 'tasks/edit_textarea.html'

    def __init__(self, *args, instance_pk=None, **kwargs):
        # Probleme instance_pk
        self.instance_pk = instance_pk
        return super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['instance_pk'] = self.instance_pk
        return context


class EditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']

    def __init__(self, *args, model_instance=None, **kwargs):

        result = super().__init__(*args, **kwargs)

        self.fields['description'] = CharField(
            initial=model_instance and model_instance.description or None,
            label=_('New Description'),
            widget=DescriptionTask(
                instance_pk=model_instance and model_instance.pk or None))

        return result

    def save(self, pk):
        Task.objects.filter(pk=pk).update(**self.cleaned_data)


class FoundationCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    # Create a new class for change template CheckboxSelectMultiple

    # Redirect for change structure with ul li
    template_name = 'tasks/multi_choice_foundation.html'
    # Redirect for change structure input label
    option_template_name = 'tasks/option_foundation.html'


class FilterForm(forms.Form):
    status = forms.MultipleChoiceField(
        choices=Task.STATUS_CHOICES,
        # Redirect to FoundationCheckboxSelectMultiple
        widget=FoundationCheckboxSelectMultiple(),
        label=_("Status"))

    def clean_my_field(self):
        if len(self.cleaned_data['my_status']) > 3:
            raise forms.ValidationError(_('Select no more than 3.'))
        return self.cleaned_data['my_status']


class StatusChoice(forms.Select):
    template_name = 'tasks/status_choice.html'

    def __init__(self, *args, instance_pk=None, **kwargs):
        self.instance_pk = instance_pk
        return super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['instance_pk'] = self.instance_pk
        return context


class UpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['status']

    def __init__(self, *args, model_instance=None, **kwargs):

        result = super().__init__(*args, **kwargs)

        self.fields['status'] = TypedChoiceField(
            choices=Task.STATUS_CHOICES,
            initial=model_instance and model_instance.status or None,
            label='',
            widget=StatusChoice(
                instance_pk=model_instance and model_instance.pk or None))

        return result

    def save(self, pk):
        Task.objects.filter(pk=pk).update(**self.cleaned_data)


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize(
            'NFKC',
            super(UsernameField, self).to_python(value))


class UserCreationForm(UserCreationFrom_):

    class Meta(UserCreationFrom_.Meta):
        fields = ("username", "email")

    def __init__(self, *args, model_instance=None, **kwargs):
        result = super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].label = ''
        return result
