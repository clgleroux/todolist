from django.shortcuts import (
    render, redirect)
from django.urls import reverse

from .models import Task
from .forms import (
    CreationForm, UpdateForm, FilterForm, UserCreationForm, EditForm)

from django.contrib import messages
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import LoginView as LoginView_

from django.contrib.auth.decorators import login_required


def hack(request):
    # FIXME - HACK: fix textarea newlines handling
    request.POST._mutable = True
    description = request.POST.get('description')
    if description:
        description = description.replace('\r\n', '\n')
        request.POST['description'] = description
    request.POST._mutable = False
    # End of HACK


# User connect required
@login_required(login_url='/')
def home(request):
    if not request.user.is_authenticated():
        # Don't connected
        return redirect('login')
    if request.method == "POST":

        hack(request)

        create_form = CreationForm(request.POST)
        if create_form.is_valid():
            # Create New Task
            obj = create_form.save(commit=False)
            obj.creator = request.user
            obj.save()
            return redirect(reverse('tasks:home'))

        else:
            # New Task is Invalid
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
        # Display status ask
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
        status=200
    )


# User connect required
@login_required(login_url='/')
def delete(request, pk):
    # Delete Task
    Task.objects.get(pk=pk).delete()
    return redirect(reverse('tasks:home'))


# User connect required
@login_required(login_url='/')
def update(request, pk):
    if request.method == "GET":
        # Update a status
        form = UpdateForm(request.GET)
        if form.is_valid():
            form.save(pk)

    elif request.method == "POST":
        # Edit Task
        hack(request)

        form_edit = EditForm(request.POST)
        if form_edit.is_valid():
            form_edit.save(pk)
    return redirect(reverse('tasks:home'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create a new User
            form.save()
            messages.success(request, 'Profile is created.')
            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'tasks/register.html', {'form': form})


def logoutnlogin(request):
    # Disconnected
    return logout_then_login(request, login_url='/login')


class LoginView(LoginView_):
    template_name = 'tasks/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            # User connected go home
            return redirect('tasks:home')
        return super().get(request, *args, **kwargs)
