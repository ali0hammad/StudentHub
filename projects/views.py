from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProjectGroup, Task, PeerHelpRequest, PeerHelpResponse
from communities.models import Course
from accounts.models import UserProfile

@login_required
def group_list(request):
    groups = ProjectGroup.objects.all().order_by('-created_at')
    my_groups = request.user.project_groups.all()
    return render(request, 'projects/group_list.html', {'groups': groups, 'my_groups': my_groups})

@login_required
def group_create(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        course_id = request.POST.get('course')

        group = ProjectGroup.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        if course_id:
            group.course = Course.objects.get(id=course_id)
            group.save()

        group.members.add(request.user)
        messages.success(request, 'Project group created successfully!')
        return redirect('projects:group_detail', group_id=group.id)

    return render(request, 'projects/group_create.html', {'courses': courses})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(ProjectGroup, id=group_id)
    tasks = group.tasks.all().order_by('deadline', 'is_completed')
    is_member = request.user in group.members.all()
    return render(request, 'projects/group_detail.html', {'group': group, 'tasks': tasks, 'is_member': is_member})

@login_required
def group_join(request, group_id):
    group = get_object_or_404(ProjectGroup, id=group_id)
    group.members.add(request.user)
    messages.success(request, f'You joined {group.name}')
    return redirect('projects:group_detail', group_id=group.id)

@login_required
def task_create(request, group_id):
    group = get_object_or_404(ProjectGroup, id=group_id)
    if request.user not in group.members.all():
        messages.error(request, 'You must be a member to add tasks.')
        return redirect('projects:group_detail', group_id=group.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        assigned_to_id = request.POST.get('assigned_to')

        task = Task(project=group, title=title, description=description)
        if deadline:
            task.deadline = deadline
        if assigned_to_id:
            task.assigned_to_id = assigned_to_id
        task.save()
        messages.success(request, 'Task added.')
        return redirect('projects:group_detail', group_id=group.id)

    return render(request, 'projects/task_create.html', {'group': group})

@login_required
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user in task.project.members.all():
        task.is_completed = not task.is_completed
        task.save()
    return redirect('projects:group_detail', group_id=task.project.id)

@login_required
def help_list(request):
    requests = PeerHelpRequest.objects.all().order_by('-created_at')
    return render(request, 'projects/help_list.html', {'requests': requests})

@login_required
def help_request_create(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course')

        help_req = PeerHelpRequest.objects.create(
            title=title,
            description=description,
            requested_by=request.user
        )
        if course_id:
            help_req.course_id = course_id
            help_req.save()
        messages.success(request, 'Help request posted.')
        return redirect('projects:help_list')

    return render(request, 'projects/help_request_create.html', {'courses': courses})

@login_required
def help_detail(request, request_id):
    help_req = get_object_or_404(PeerHelpRequest, id=request_id)
    if request.method == 'POST':
        message = request.POST.get('message')
        PeerHelpResponse.objects.create(
            help_request=help_req,
            responder=request.user,
            message=message
        )
        messages.success(request, 'Response added.')
        return redirect('projects:help_detail', request_id=help_req.id)

    return render(request, 'projects/help_detail.html', {'help_req': help_req})

@login_required
def find_partners(request):
    course_q = request.GET.get('course', '')
    users = []

    if course_q:
        # A simple matching algorithm: search users who mentioned course in their interests, or just search all profiles
        users = UserProfile.objects.filter(interests__icontains=course_q).exclude(user=request.user)

    return render(request, 'projects/find_partners.html', {'users': users, 'course_q': course_q})
