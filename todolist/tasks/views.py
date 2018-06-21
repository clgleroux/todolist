from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import (
    CreationForm, UpdateForm, FilterForm)

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import logout_then_login


def home(request):
    if not request.user.is_authenticated():
        return redirect('login')
    if request.method == "POST":
        create_form = CreationForm(request.POST)
        if create_form.is_valid():
            obj = create_form.save(commit=False)
            obj.creator = request.user
            obj.save()
            return redirect(reverse('tasks:home'))
        else:
            return render(
                request,
                'tasks/index.html',
                {'create_form': create_form},
                status=400)

    create_form = CreationForm()
    filter_form = FilterForm()

    global tasks
    tasks = None
    tasks = Task.objects.all().filter(creator=request.user).order_by('-pk')

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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})


def logoutnlogin(request):
    return logout_then_login(request, login_url='/login')
