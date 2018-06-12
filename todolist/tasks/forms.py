from django import forms
from django.forms import ModelForm
from tasks.models import Task


class CreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']


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


class SelectForm(forms.Form):
    status = forms.MultipleChoiceField(
        choices=Task.STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple())

    def clean_my_field(self):
        if len(self.cleaned_data['my_status']) > 3:
            raise forms.ValidationError('Select no more than 3.')
        return self.cleaned_data['my_status']
