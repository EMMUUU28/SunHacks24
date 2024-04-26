from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Skill)

admin.site.register(JobOpening)
admin.site.register(AppliedJob)