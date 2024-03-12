from django.urls import path
from .views import clients_list,client_add,client_detail,client_edit,client_delete,add_comment,client_add_file,client_export

app_name = 'clients'


urlpatterns = [
    path('',clients_list,name='list'),
    path('add_client/',client_add,name='add'),
    path('<int:pk>/',client_detail,name='detail'),
    path('<int:pk>/edit/',client_edit,name='edit'),
    path('<int:pk>/add-comment/',add_comment,name='add_comments'),
    path('<int:pk>/add-file/',client_add_file,name='add_files'),
    path('<int:pk>/delete/',client_delete,name='delete'),
    path('export/',client_export,name='export')
]