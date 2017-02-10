from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime

class project(models.Model):
    title = models.CharField(max_length=200)
    clientname = models.CharField(max_length=200)
    projectname = models.CharField(max_length=200)
    services = models.CharField(max_length=200)
    startdate = models.DateField()
    enddate = models.DateField()
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)

class projectmedia(models.Model):
    file = models.FileField(upload_to='projects')
    project = models.ForeignKey(project, on_delete=models.CASCADE)

