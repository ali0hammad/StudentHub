from django.urls import path
from . import views

app_name = 'engagement'

urlpatterns = [
    path('confessions/', views.confession_board, name='confessions'),
    path('appreciations/', views.appreciation_board, name='appreciations'),
    path('polls/', views.poll_list, name='polls'),
    path('polls/<int:poll_id>/vote/', views.poll_vote, name='poll_vote'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('meet-batchmate/', views.meet_batchmate, name='meet_batchmate'),
]
