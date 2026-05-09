from django.contrib import admin
from .models import ProjectGroup, Task, PeerHelpRequest, PeerHelpResponse

admin.site.register(ProjectGroup)
admin.site.register(Task)
admin.site.register(PeerHelpRequest)
admin.site.register(PeerHelpResponse)
