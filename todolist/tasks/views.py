from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import (
    CreationForm, UpdateForm, FilterForm)


def home(request):
    if request.method == "POST":
        create_form = CreationForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect(reverse('tasks:home'))
        else:
            return render(
                request,
                'tasks/index.html',
                {'create_form': create_form},
                status=400)

    create_form = CreationForm()
    filter_form = FilterForm()
    tasks = Task.objects.all().order_by('-pk')

    if 'status' in request.GET:
        tasks = tasks.filter(status__in=request.GET.getlist('status'))
        filter_form = FilterForm(request.GET)

    return render(
        request,
        'tasks/index.html',
        {
            'create_form': create_form,
            'filter_form': filter_form,
            'tasks': tasks,
        },
    )


def delete(request, pk):
    Task.objects.get(pk=pk).delete()
    return redirect(reverse('tasks:home'))


def update(request, pk):
    if request.method == "GET":
        form = UpdateForm(request.GET)
        if form.is_valid():
            form.save(pk)
    return redirect(reverse('tasks:home'))
