from django.forms import ModelForm
from tasks.models import Task


class CreationForm(ModelForm):
    class Meta:
        model = Task
        fields = ['description']
