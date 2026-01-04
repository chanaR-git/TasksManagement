from django.shortcuts import render

from TasksManagementApp.models import Employee
from TasksManagementApp.forms import loginForm, EmployeeCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse

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
    return render(request,'tasks.html')

