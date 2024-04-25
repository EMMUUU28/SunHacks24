from django.contrib import admin

# Register your models here.
from . models import Education,WorkExperience,Skill

admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Skill)