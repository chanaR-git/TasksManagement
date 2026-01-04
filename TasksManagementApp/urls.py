from django.urls import path

from TasksManagementApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register, name='register'),
    path("login", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("tasks", views.tasks, name='tasks'),
    path("add_task", views.add_task, name='add_task'),
    path("edit_task/<int:task_id>", views.edit_task, name='edit_task'),
    path("delete_task/<int:task_id>", views.delete_task, name='delete_task'),
    path("take_task/<int:task_id>", views.take_task, name='take_task'),
    path("complete_task/<int:task_id>", views.complete_task, name='complete_task'),
]