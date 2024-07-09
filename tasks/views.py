from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home.html', {
    })

def signup(request):
    if (request.method == 'GET'):
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if (request.POST['password1']==request.POST['password2']):
            try:
                user = User.objects.create_user(username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe.'
                })
        return render(request, 'signup.html',{
                'form': UserCreationForm,
                'error': 'Contraseñas no coinciden.'
            })
@login_required
def tasks(request):
    tasks = Task.objects.filter(usuario=request.user, fecha_termino__isnull=True)
    return render(request, 'tasks.html',{'tasks':tasks})
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(usuario=request.user, fecha_termino__isnull=False).order_by('-fecha_termino')
    return render(request, 'tasks.html',{'tasks':tasks})
@login_required
def crear_tarea(request):
    if (request.method == 'GET'):
        return render(request,'crear_tarea.html',{
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.usuario = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'crear_tarea.html',{
                'form': TaskForm,
                'error': 'Por favor ingrese datos validos'
            })            
@login_required
def task_detail(request,task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=task_id, usuario=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task,pk=task_id, usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form,
            'error': 'Error al modificar la tarea.'})
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario = request.user)
    if request.method == 'POST':
        task.fecha_termino = timezone.now()
        task.save()
        return redirect('tasks')
@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, usuario = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if (request.method == 'GET'):
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST
            ['password'])
        if (user is None):
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o Contraseña incorrectos.'
            })
        else:
            login(request, user)
            return redirect('tasks')