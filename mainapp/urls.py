from django.contrib import admin
from django.urls import path,include
from . import views 
urlpatterns = [
    path('',views.home,name="index"),
    # path('test/',views.index,name="index"),
    path('applyjob/',views.applyjob,name="applyjob"),
    path("addworkexp/",views.addworkexp,name='addworkexp'),
    path("addeducation/",views.addeducation,name='addeducation'),
    path("addskills/",views.addskills,name='addskills'),
    path("applicants/",views.applicants,name='applicants'),
    path("addjob/",views.addJob,name="addJob"),
    path("listjob/",views.listjob,name="listjob"),
    path("profile/",views.profile,name="profile")
]