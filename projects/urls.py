from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('groups/', views.group_list, name='group_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.group_join, name='group_join'),
    path('groups/<int:group_id>/add-task/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
    path('peer-help/', views.help_list, name='help_list'),
    path('peer-help/request/', views.help_request_create, name='help_request_create'),
    path('peer-help/<int:request_id>/', views.help_detail, name='help_detail'),
    path('find-partners/', views.find_partners, name='find_partners'),
]
