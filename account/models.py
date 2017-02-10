from django.db import models
from django.contrib.auth.models import User


class Userprofile(models.Model):
    address = models.CharField(max_length=200)
    ext = models.CharField(max_length=20,default='')
    phoneno = models.CharField(max_length=200,default='')
    mobileno = models.CharField(max_length=200)
    profilepic = models.FileField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)
    aboutme =  models.CharField(max_length=2000,default='')
    skills = models.CharField(max_length=1000,default='')
    emailverified = models.BooleanField(default=False)
    position = models.CharField(max_length=1000)
    skypeid = models.CharField(max_length=1000)
    membertype = models.CharField(max_length=1000, default='INDIVIDUAL');

    def skillstolist(self):
        return self.skills.split(',')

class contactrequest(models.Model):
    fromuser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='fromuser')
    touser = models.ForeignKey(User, on_delete=models.CASCADE,related_name='touser')
    status = models.CharField(max_length=200,default='PENDING')
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

class usercontact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    contact = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contact')
    status = models.CharField(max_length=200,default='ACCEPTED')
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)