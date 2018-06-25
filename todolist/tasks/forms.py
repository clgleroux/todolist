from django import forms

import unicodedata

from django.forms import ModelForm
from django.forms.fields import TypedChoiceField
from django.forms import EmailField

from tasks.models import Task
from django.utils.translation import gettext_lazy as _


from django.contrib.auth import password_validation

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm as UserCreationFrom_


class CreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']
        labels = {
            "description": _("Description"),
        }


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


class FoundationSelectForm(forms.Select):
    template_name = 'tasks/select_choice_foundation.html'

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
            widget=FoundationSelectForm(
                instance_pk=model_instance and model_instance.pk or None))

        return result

    def save(self, pk):
        Task.objects.filter(pk=pk).update(**self.cleaned_data)


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class UserCreationForm(UserCreationFrom_):
    email = EmailField(label=_(""), required=True)
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput,
        # TODO: Surcharge de la password_validators_help_text_html
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
