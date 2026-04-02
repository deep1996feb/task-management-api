from django.urls import path
from .views import *


urlpatterns = [
    
    path("tasks/", CreateTaskAPI.as_view(), name="task"),
    
    path('tasks_list/', TaskListAPI.as_view()),
    
    path('tasks_detail/<int:pk>/', TaskDetailAPI.as_view()),
    
    path('tasks/<int:pk>/update/', TaskUpdateAPI.as_view()),
    
    path('tasks/<int:pk>/delete/', TaskDeleteAPI.as_view()),
    
]