from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class team(models.Model):
    teamname = models.CharField(max_length=200, default='')
    aboutteam = models.CharField(max_length=200, default='')
    hostedteamid = models.CharField(max_length=200, default='')
    logo = models.FileField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200,default='ACTIVE')
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class teaminvites(models.Model):
    team = models.ForeignKey(team, on_delete=models.CASCADE,related_name='invitedteam')
    status = models.CharField(max_length=200, default='PENDING')
    inviteduser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='inviteduser')
    deleted = models.BooleanField(default=False)


class relTeamContact(models.Model):
    team = models.ForeignKey(team, on_delete=models.CASCADE,related_name='team')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='member')