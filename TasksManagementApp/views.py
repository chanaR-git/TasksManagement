from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from TasksManagementApp.models import Employee, Task, Team
from TasksManagementApp.forms import loginForm, EmployeeCreationForm , AddTaskForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.exceptions import ValidationError


def register(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # עדכון משתמש קיים
            form = EmployeeCreationForm(request.POST, instance=request.user)
        else:
            # יצירת משתמש חדש
            form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            print("Form errors:", form.errors)
    else:
        if request.user:
            form = EmployeeCreationForm(instance=request.user)
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

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def tasks(request):
    user = request.user
    role = user.employee_role

    employees = Employee.objects.all()
    tasks_qs = get_tasks_for_current_user(request)

    # סינון
    status = request.GET.get('status')
    employee = request.GET.get('employee')
    if status:
        tasks_qs = tasks_qs.filter(task_status=status)
    if employee:
        tasks_qs = tasks_qs.filter(employee_id=employee)

    return render(request, 'tasks.html', {
        'user': user,
        'role': role,
        'tasks': tasks_qs,
        'employees': employees,
        'form': AddTaskForm(),
    })

def get_tasks_for_current_user(request):
        return Task.objects.filter(task_team=request.user.team_code)

# @require_POST
@login_required
def add_task(request):
    if request.user.employee_role != 1:
        return redirect('tasks')
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_status = 1 # Set status to new
            task.task_team = request.user.team_code
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('tasks')
        else:
            employees = Employee.objects.all()
            tasks_qs = Task.objects.filter(task_team=request.user.team_code)
            messages.error(request, 'המשימה לא נשמרה. נא לבדוק את השדות ולנסות שוב.')
            return render(request, 'tasks.html', {
                'user': request.user,
                'role': request.user.employee_role,
                'tasks': tasks_qs,
                'employees': employees,
                'form': form,
                'open_modal': True,  # משתנה לפתיחת המודל
            })
            print("Form errors:", form.errors)
    else:
        return redirect('tasks')

@require_POST
@login_required
def delete_task(request, task_id):
    if request.user.employee_role != 1:
        return redirect('tasks')
    task = get_object_or_404(Task, pk=task_id)
    # if (task.employee is not None):
    #     return redirect('tasks')
    task.delete()
    return redirect('tasks')

@require_POST
@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not task.employee:
        task.employee = request.user
        task.task_status = 2  # Set status to in process
        task.save()
    return redirect('tasks')

@require_POST
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.employee == request.user:
        task.task_status = 3  # Set status to completed
        task.task_completed_date = timezone.now()
        task.save()
    return redirect('tasks')

@login_required
def edit_task(request, task_id):
    if request.user.employee_role != 1:
        return redirect('tasks')
    task = get_object_or_404(Task, pk=task_id)
    if request.method =='POST':
        task.task_name = request.POST.get('task_name')
        task.task_description = request.POST.get('task_description')
        task.task_last_date = request.POST.get('task_last_date')
        # if task.task_last_date < timezone.now().date():
        #     task.task_last_date = timezone.now().date()
        task.save()
        return redirect('tasks')
    return render(request,'edit_task.html',{'task':task})


