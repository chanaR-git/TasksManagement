from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee,Team,Task
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
    team_code= forms.ModelChoiceField(queryset=Team.objects.all(),empty_label=None)

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'task_last_date', 'employee']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'task_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'task_last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
        }
    task_last_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))