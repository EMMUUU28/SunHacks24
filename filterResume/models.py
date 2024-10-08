from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.question[:20]}'
    

class Jobinfo(models.Model):
    job_description=models.TextField()
    type=models.TextField()