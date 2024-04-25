from django.db import models

# Create your models here.
class JobOpening(models.Model):
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    deadline_date = models.DateField()