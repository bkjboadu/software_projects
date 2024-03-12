from django.urls import path
from . import api_views

urlpatterns = [
    path('',api_views.post_list, name='post_list'),
    path('create/',api_views.post_create,name='post_create'),
    path('profile/<str:id>',api_views.post_list_profile,name='post_list_profile'),
]