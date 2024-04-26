from django.contrib import admin
from django.urls import path,include
from . import views 
urlpatterns = [
    path('filter/',views.filtering,name="filtering"),
    path('resumeassistant/',views.resumeassistant,name="resumaassistant"),
    path('filterlist/',views.filterlist,name="filterlist"),
    path('mystral/',views.main,name="main"),
]