from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportPost, SupportComment, MentorMatching, SocialWallPost

@login_required
def support_board(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        SupportPost.objects.create(title=title, content=content)
        messages.success(request, 'Support request posted anonymously.')
        return redirect('support:support_board')

    posts = SupportPost.objects.all().order_by('-created_at')
    return render(request, 'support/support_board.html', {'posts': posts})

@login_required
def support_post_detail(request, post_id):
    post = get_object_or_404(SupportPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        SupportComment.objects.create(post=post, content=content)
        messages.success(request, 'Comment added anonymously.')
        return redirect('support:support_post_detail', post_id=post.id)

    return render(request, 'support/support_detail.html', {'post': post})

@login_required
def mentor_match(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        department = request.POST.get('department')
        expertise = request.POST.get('expertise_needs')

        # Prevent multiple active profiles
        MentorMatching.objects.filter(user=request.user).delete()

        MentorMatching.objects.create(
            user=request.user,
            role=role,
            department=department,
            expertise_needs=expertise
        )
        messages.success(request, 'Your mentorship profile has been updated.')
        return redirect('support:mentor_match')

    mentors = MentorMatching.objects.filter(role='mentor').exclude(user=request.user).order_by('-created_at')
    mentees = MentorMatching.objects.filter(role='mentee').exclude(user=request.user).order_by('-created_at')

    my_profile = MentorMatching.objects.filter(user=request.user).first()

    return render(request, 'support/mentor_match.html', {
        'mentors': mentors,
        'mentees': mentees,
        'my_profile': my_profile
    })

@login_required
def social_wall(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            SocialWallPost.objects.create(author=request.user, content=content)
            messages.success(request, 'Posted to social wall.')
            return redirect('support:social_wall')

    posts = SocialWallPost.objects.all().order_by('-created_at')

    # Simple daily prompt logic
    prompts = [
        "What's your favorite spot on campus?",
        "Who is the toughest professor in your department?",
        "What's the best memory from your first semester?",
        "Share a study tip that always works for you."
    ]
    import random
    daily_prompt = random.choice(prompts)

    return render(request, 'support/social_wall.html', {'posts': posts, 'daily_prompt': daily_prompt})
