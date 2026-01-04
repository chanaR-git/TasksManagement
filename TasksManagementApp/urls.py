from django.urls import path

from TasksManagementApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.register),
    path("login",auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("tasks",views.tasks,name='tasks'),
   # path("tasks/<int:id>",views.tasks),

]