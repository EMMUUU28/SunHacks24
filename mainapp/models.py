from django.db import models
from django.contrib.auth.models import User  # Import the User model from Django's built-in authentication system


# Create your models here.
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_date = models.CharField(max_length=7)  # Change the field to CharField with max_length 7 for "YYYY-MM"
    end_date = models.CharField(max_length=7)
    # Add more fields as needed for education details

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    # Add more fields as needed for work experience

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    skill_name = models.CharField(max_length=100)
    # Add more fields as needed for skills


class AppliedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    file = models.FileField(upload_to='uploads/')
    