from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('account/',include('userprofile.urls'),name='userprofile'),
    path('dashboard/',include('dashboard.urls')),
    path('dashboard/leads/',include('lead.urls')),
    path('dashboard/client/',include('client.urls')),
    path('dashboard/team/',include('team.urls')),
    path('',include('core.urls'),name='core'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

