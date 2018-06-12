from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import CreationForm


def home(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            return render(
                request,
                'tasks/index.html',
                {'form': form},
                status=400)
    else:
        form = CreationForm()
    # return redirect(reverse('home'), {'form': form})
    return render(
        request,
        'tasks/index.html',
        {'form': form, 'tasks': Task.objects.all()},
        )
