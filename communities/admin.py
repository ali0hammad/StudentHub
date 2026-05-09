from django.contrib import admin
from .models import Department, Course, CourseRoom, Message, Resource

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CourseRoom)
admin.site.register(Message)
admin.site.register(Resource)
