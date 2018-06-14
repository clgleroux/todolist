from django import forms
from django.forms import ModelForm
from tasks.models import Task
from django.utils.translation import gettext_lazy as _


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


class UpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['status']

    def __init__(self, *args, model_instance=None, **kwargs):
        initial = {}
        if model_instance is not None:
            initial['status'] = model_instance.status
        return super().__init__(*args, initial=initial, **kwargs)

    def save(self, pk):
        Task.objects.filter(pk=pk).update(**self.cleaned_data)
