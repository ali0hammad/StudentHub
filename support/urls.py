from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('peer-support/', views.support_board, name='support_board'),
    path('peer-support/<int:post_id>/', views.support_post_detail, name='support_post_detail'),
    path('mentorship/', views.mentor_match, name='mentor_match'),
    path('social-wall/', views.social_wall, name='social_wall'),
]
