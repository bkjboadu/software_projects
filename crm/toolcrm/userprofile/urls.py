from django.urls import path,include
from .views import signup,myaccount
from django.contrib.auth import views
from .form import LoginForm

app_name = 'userprofile'


urlpatterns = [
    path('sign-up/',signup,name='signup'),
    path('log-in/',views.LoginView.as_view(template_name='userprofile/login.html',authentication_form=LoginForm),name='login'),
    path('log-out/',views.LogoutView.as_view(),name='logout'),
    path('',myaccount,name='myaccount')

]