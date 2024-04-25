from django.contrib import admin
from django.urls import path,include
from . import views 
urlpatterns = [
    path('test/',views.index,name="index"),
    path('add_job/',views.adduser, name="useradd"),
    path('jobs/',views.jobs, name="jobs")
    
]