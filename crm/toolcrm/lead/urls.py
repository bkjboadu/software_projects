from django.urls import path
from .views import convert_to_client,leads_delete
from .views import LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView
from .views import AddCommentView,AddFileView,lead_export

app_name = 'leads'
urlpatterns = [
    path('<int:pk>/',LeadDetailView.as_view(),name='detail'),
    path('add-lead/',LeadCreateView.as_view(),name='add'),
    path('<int:pk>/delete/',leads_delete,name='delete'),
    path('<int:pk>/edit/',LeadUpdateView.as_view(),name='edit'),
    path('<int:pk>/add-comment/',AddCommentView.as_view(),name='add_comments'),
    path('<int:pk>/add-file/',AddFileView.as_view(),name='add_files'),
    path('<int:pk>/convert/',convert_to_client,name='convert'),
    path('',LeadListView.as_view(),name='list'),
    path('export/',lead_export,name='export')
]