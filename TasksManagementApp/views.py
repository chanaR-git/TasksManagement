from django.shortcuts import render

from TasksManagementApp.models import Employee


def register(request):
    employee = Employee.objects.all()
    return render(request,'register.html')
