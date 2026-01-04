from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from TasksManagementApp.models import Employee, Task, Team
from TasksManagementApp.forms import loginForm, EmployeeCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST

def register(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        print("form valid", form.is_valid())
        if form.is_valid():
            print("Form data:", form.cleaned_data)
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print("Form errors:", form.errors)
    else:
        form = EmployeeCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if(request.method=='POST'):
        form = loginForm(request.POST)
        print("form valid",form.is_valid())
        if(form.is_valid()):
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print("Username:", username, "Password:", password)
            try:
                user= authenticate(username=username,password=password)
                print("User:",user)
                if user is not None:
                    form.save()
                    auth_login(request,user)
                    return redirect('tasks')
            except Exception as e:
                messages.error(request,'Invalid username or password')   
    form=loginForm()
    return render(request,'login.html',{'form':form})

def tasks(request):
    user = request.user
    employees = Employee.objects.filter(team_code=user.team_code) if user.team_code else []
    if user.employee_role == 1:  # מנהל     
        tasks = Task.objects.filter(task_team=user.team_code)
    else:  # עובד
        tasks = Task.objects.filter(task_team=user.team_code)
    return render(request, 'tasks.html', {
        'user': user,
        'role': user.employee_role,
        'tasks': tasks,
        'employees': employees,
    })

@login_required
def add_task(request):
    # טופס הוספת משימה (פשוט)
    if request.method == 'POST':
        name = request.POST.get('task_name')
        desc = request.POST.get('task_description')
        date = request.POST.get('task_last_date')
        team = request.user.team_code
        Task.objects.create(task_name=name, task_description=desc, task_last_date=date, task_completed_date=date, task_status=1, task_team=team, employee=None)
        return redirect('tasks')
    return render(request, 'add_task.html')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.task_name = request.POST.get('task_name')
        task.task_description = request.POST.get('task_description')
        task.task_last_date = request.POST.get('task_last_date')
        task.save()
        return redirect('tasks')
    return render(request, 'edit_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return HttpResponse('Method not allowed', status=405)

@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST' and request.user.employee_role == 2 and not task.employee:
        task.employee = request.user
        task.task_status = 2
        task.save()
        return redirect('tasks')
    return HttpResponse('Method not allowed', status=405)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST' and request.user == task.employee:
        task.task_status = 3
        task.save()
        return redirect('tasks')
    return HttpResponse('Method not allowed', status=405)

