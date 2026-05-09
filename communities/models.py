from django.db import models
from accounts.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

class CourseRoom(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='room')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course.name} Room"

class Message(models.Model):
    room = models.ForeignKey(CourseRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.email} in {self.room}"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('note', 'Note'),
        ('past_paper', 'Past Paper'),
        ('lab_manual', 'Lab Manual'),
        ('assignment', 'Assignment'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    description = models.TextField(blank=True)
    external_link = models.URLField() # Links only, no file uploads
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"
