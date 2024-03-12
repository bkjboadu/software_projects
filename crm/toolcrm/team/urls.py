from django.urls import path
from .views import edit_team,detail,teams_activate,teams_list

app_name = 'teams'

urlpatterns = [
    path('<int:pk>/edit/',edit_team,name='edit'),
    path('<int:pk>/detail/',detail,name='detail'),
    path('<int:pk>/activate/',teams_activate,name='activate'),
    path('',teams_list,name='list')
]