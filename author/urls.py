from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/',views.register, name ='registration'),
    # path('login/',views.user_login, name ='loginPage'),
    path('login/',views.UserLoginView.as_view(), name ='loginPage'),
    # path('logout/',views.user_logout, name ='logoutPage'),
    path('logout/',views.LogoutView.as_view(), name ='logoutPage'),
    path('profile/',views.profile, name ='profilePage'),
    path('profile/pass_change/',views.pass_change, name ='change_password'),
    path('profile/update_profile/',views.u_profile, name ='updateProfile'),
]
