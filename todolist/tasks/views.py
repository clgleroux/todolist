from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import CreationForm


def home(request):
    return render(
        request,
        'tasks/index.html',
        {'tasks': Task.objects.all()},
    )


def create(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'), status=201)
        else:
            return render(
                request,
                'tasks/create.html',
                {'form': form},
                status=400)
    else:
        form = CreationForm()
    return render(request, 'tasks/create.html', {'form': form})
