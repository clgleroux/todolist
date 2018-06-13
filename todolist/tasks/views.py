from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import (
    CreationForm, UpdateForm, SelectForm)


def home(request):
    if request.method == "POST":
        create_form = CreationForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect(reverse('home'))
        else:
            return render(
                request,
                'tasks/index.html',
                {'create_form': create_form},
                status=400)

    create_form = CreationForm()
    select_form = SelectForm()
    tasks = Task.objects.all().order_by('-pk')

    if 'status' in request.GET:
        tasks = tasks.filter(status__in=request.GET.getlist('status'))
        select_form = SelectForm(request.GET)

    return render(
        request,
        'tasks/index.html',
        {
            'create_form': create_form,
            'select_form': select_form,
            'tasks': tasks,
        },
    )


def delete(request, pk):
    Task.objects.get(pk=pk).delete()
    return redirect(reverse('home'))


def update(request, pk):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            form.save(pk)
    return redirect(reverse('home'))
