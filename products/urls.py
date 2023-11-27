from django.urls import path

from .views import (
    reportList, reportCreate, reportUpdate, reportListMaintainance,
    delete_image, delete_VechilePart, task_list, create_task, 
    edit_task, delete_task
)

app_name = 'reports'  # 3rd

urlpatterns = [
    path('', reportList, name='list_reports'),
    path('user-specific-reports/', reportListMaintainance, name='specific_list_reports'),
    path('create/', reportCreate.as_view(), name='create_report'),
    path('update/<int:pk>/', reportUpdate.as_view(), name='update_report'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-VechilePart/<int:pk>/', delete_VechilePart, name='delete_VechilePart'),


    path('tasks', task_list, name='task-list'),
    path('tasks/create/', create_task, name='create-task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit-task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete-task'),
]
