from django.urls import path

from TasksManagementApp import views

urlpatterns = [
    path("register", views.register),
    path("login",views.login),
    path("tasks",views.tasks),
   # path("tasks/<int:id>",views.tasks),

]