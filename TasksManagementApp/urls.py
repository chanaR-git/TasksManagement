from django.urls import path

from TasksManagementApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name='register'),
    path("login", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('take_task/<int:task_id>/', views.take_task, name='take_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]