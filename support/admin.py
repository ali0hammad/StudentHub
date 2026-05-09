from django.contrib import admin
from .models import SupportPost, SupportComment, MentorMatching, SocialWallPost

admin.site.register(SupportPost)
admin.site.register(SupportComment)
admin.site.register(MentorMatching)
admin.site.register(SocialWallPost)
