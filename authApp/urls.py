
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from authApp import views

urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user_logout',views.user_logout,name="user_logout"),
    # path('social-auth', include('social_django.urls', namespace='social')),
    # path("authhome/", views.home, name='home'),
    path('user_register/',views.user_register,name='user_register'),
]
