from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    oldPic = models.ImageField(upload_to='waste/')
    newPic = models.ImageField(upload_to='result/', blank=True, null=True)
    desc = models.TextField(max_length=250)
    title = models.CharField(max_length=100)
    state = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recordedTime = models.DateTimeField(auto_now_add=True)