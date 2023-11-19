from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("create_report", views.band_create, name="create-report"),
    path('tasks', views.task_list, name='task-list'),
    path('tasks/create/', views.create_task, name='create-task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit-task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete-task'),
]