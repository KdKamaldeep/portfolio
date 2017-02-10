from django.db import models
from django.contrib.auth.models import User
from project import models as projectmodel

class portFolio(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    uuid = models.CharField(max_length=200, default='')
    desc = models.CharField(max_length=4000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    snapshot = models.FileField(upload_to='portfolios')

class portfolioItem(models.Model):
    portfolio = models.ForeignKey(portFolio, on_delete=models.CASCADE)
    projectname = models.CharField(max_length=200)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    desc = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)

class portfolioItemMedia(models.Model):
    portfolioitem = models.ForeignKey(portfolioItem, on_delete=models.CASCADE)
    mediapath = models.FileField(upload_to='portfoliomedia')
    mediatype = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    lastupdate_date = models.DateTimeField(auto_now_add=True)

class relProjectPortfolio(models.Model):
    portfolio = models.ForeignKey(portFolio, on_delete=models.CASCADE)
    project = models.ForeignKey(projectmodel.project, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

