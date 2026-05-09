from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Department, Course, CourseRoom, Resource, Message
from django.contrib import messages

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'communities/department_list.html', {'departments': departments})

@login_required
def department_detail(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    courses = department.courses.all()
    return render(request, 'communities/department_detail.html', {'department': department, 'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    resources = course.resources.all().order_by('-created_at')

    # Query logic for searching resources
    q = request.GET.get('q')
    if q:
        resources = resources.filter(title__icontains=q)

    return render(request, 'communities/course_detail.html', {'course': course, 'resources': resources})

@login_required
def add_resource(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        resource_type = request.POST.get('resource_type')
        description = request.POST.get('description')
        external_link = request.POST.get('external_link')

        Resource.objects.create(
            course=course,
            title=title,
            resource_type=resource_type,
            description=description,
            external_link=external_link,
            uploaded_by=request.user
        )
        messages.success(request, 'Resource added successfully!')
        return redirect('communities:course_detail', course_id=course.id)

    return render(request, 'communities/add_resource.html', {'course': course, 'resource_types': Resource.RESOURCE_TYPES})

@login_required
def course_room(request, room_id):
    room = get_object_or_404(CourseRoom, id=room_id)
    recent_messages = room.messages.order_by('timestamp')[:50]
    return render(request, 'communities/room.html', {
        'room': room,
        'recent_messages': recent_messages,
    })
