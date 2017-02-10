from django.shortcuts import render_to_response
from project import models as projectmodel
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required(login_url=settings.LOGIN_URL)
def index(request):
    projects = projectmodel.project.objects.all()
    return render_to_response(
        'dashboard/dashboard.html',
        {'projects': projects});