from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('department/<int:dept_id>/', views.department_detail, name='department_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('room/<int:room_id>/', views.course_room, name='course_room'),
    path('course/<int:course_id>/add-resource/', views.add_resource, name='add_resource'),
]
