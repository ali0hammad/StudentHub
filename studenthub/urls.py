from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('support/', include('support.urls')),
    path('campus/', include('campus.urls')),
    path('engagement/', include('engagement.urls')),
    path('projects/', include('projects.urls')),
    path('communities/', include('communities.urls')),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
]
