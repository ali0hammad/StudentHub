from django.urls import path
from . import views

app_name = 'campus'

urlpatterns = [
    path('events/', views.event_list, name='events'),
    path('events/add/', views.event_create, name='event_create'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/add/', views.marketplace_create, name='marketplace_create'),
    path('lost-found/', views.lost_found_list, name='lost_found'),
    path('lost-found/add/', views.lost_found_create, name='lost_found_create'),
    path('rides/', views.rideshare_list, name='rides'),
    path('rides/add/', views.rideshare_create, name='rideshare_create'),
]
