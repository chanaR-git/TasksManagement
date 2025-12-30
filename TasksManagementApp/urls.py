from django.urls import path

from TasksManagementApp import views

urlpatterns = [
    path("register", views.register),
]
