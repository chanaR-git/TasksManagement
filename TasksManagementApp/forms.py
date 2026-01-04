from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee
from django.contrib.auth.models import User

class loginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        fields = ['username', 'password']

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['username', 'employee_role', 'team_code']