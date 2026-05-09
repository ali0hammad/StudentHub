from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Confession, Appreciation, Poll, PollOption, PollVote, LeaderboardStat
from accounts.models import UserProfile
import random

@login_required
def confession_board(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Confession.objects.create(content=content)
            messages.success(request, 'Confession posted anonymously.')
            return redirect('engagement:confessions')

    confessions = Confession.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'engagement/confessions.html', {'confessions': confessions})

@login_required
def appreciation_board(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient_name')
        content = request.POST.get('content')
        if recipient and content:
            Appreciation.objects.create(recipient_name=recipient, content=content)
            messages.success(request, 'Appreciation posted anonymously.')
            return redirect('engagement:appreciations')

    appreciations = Appreciation.objects.all().order_by('-created_at')
    return render(request, 'engagement/appreciations.html', {'appreciations': appreciations})

@login_required
def poll_list(request):
    polls = Poll.objects.filter(is_active=True).order_by('-created_at')
    # Attach user vote status
    for poll in polls:
        poll.user_voted = poll.votes.filter(user=request.user).exists()
    return render(request, 'engagement/polls.html', {'polls': polls})

@login_required
def poll_vote(request, poll_id):
    if request.method == 'POST':
        poll = get_object_or_404(Poll, id=poll_id)
        option_id = request.POST.get('option')

        if PollVote.objects.filter(poll=poll, user=request.user).exists():
            messages.error(request, 'You have already voted on this poll.')
            return redirect('engagement:polls')

        if option_id:
            option = get_object_or_404(PollOption, id=option_id, poll=poll)
            PollVote.objects.create(poll=poll, option=option, user=request.user)
            messages.success(request, 'Vote recorded.')

    return redirect('engagement:polls')

@login_required
def leaderboard(request):
    # Get top 10 users by points
    leaders = LeaderboardStat.objects.all().select_related('user').order_by('-points')[:10]
    return render(request, 'engagement/leaderboard.html', {'leaders': leaders})

@login_required
def meet_batchmate(request):
    user_batch = request.user.profile.batch
    if not user_batch:
        messages.warning(request, "Please update your batch in your profile first.")
        return redirect('accounts:profile')

    batchmates = UserProfile.objects.filter(batch=user_batch).exclude(user=request.user)

    random_batchmate = None
    if batchmates.exists():
        random_batchmate = random.choice(list(batchmates))

    return render(request, 'engagement/meet_batchmate.html', {'batchmate': random_batchmate})
