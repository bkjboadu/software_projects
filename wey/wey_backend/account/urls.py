from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import api_views

urlpatterns = [
    path('me/',api_views.me,name='me'),
    path('signup/',api_views.signup, name='signup'),
    path('login/',TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/request/<uuid:pk>/',api_views.send_friend_request, name='send_friend_request'),
    path('friends/<uuid:pk>/',api_views.friends,name='friends'),
    path('friends/<uuid:pk>/<str:status>/',api_views.handle_request,name='handle_request')
]