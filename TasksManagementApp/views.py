from django.shortcuts import render

from TasksManagementApp.models import Employee


def register(request):
    employee = Employee.objects.all()
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def tasks(request):
    return render(request,'tasks.html')