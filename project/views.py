from django.shortcuts import render_to_response,render
from project import forms as projform
from django.http import HttpResponseRedirect
from project import models as projectmodel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from portfolio import models as portmodel
from account import models as accountmoel
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url=settings.LOGIN_URL)
def create(request):
    if request.method == "POST":
        form = projform.projectform(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)

            user = User.objects.get(pk=request.user.id)
            project.user = user
            project.save()

            if len(form.cleaned_data['projectpic']) > 0:
                medias = projectmodel.projectmedia.objects.filter(project__id=project.id)
                for media in medias:
                    media.delete()

                for each in form.cleaned_data['projectpic']:
                    media = projectmodel.projectmedia()
                    media.file = each
                    media.project = project
                    media.save()

            return HttpResponseRedirect('/project/')
        else:
            return render(request,'project/create.html', {'form': form});
    else:
        form = projform.projectform()
        return render(request, 'project/create.html', {'form': form});

@login_required(login_url=settings.LOGIN_URL)
def index(request):
    userid = request.user.id
    projects = projectmodel.project.objects.filter(user__id = userid, deleted=False)
    for project in projects:
        project.projectmedia_set.all()

    return render_to_response('project/index.html', {'request':request,'projects': projects});

@login_required(login_url=settings.LOGIN_URL)
def view(request, projectid):
    project = projectmodel.project.objects.get(pk = projectid, user__id = request.user.id)
    services = project.services.split(',')

    profile = accountmoel.Userprofile()
    try:
        profile = accountmoel.Userprofile.objects.get(user__id=project.user.id)
    except Exception as ObjectDoesNotExist:
        profile = accountmoel.Userprofile()

    return render(request, 'public/viewproject.html', {'request':request,'project': project,'services':services,'userprofile':profile });

@login_required(login_url=settings.LOGIN_URL)
def remove(request, projectid):
    project = projectmodel.project.objects.get(pk=projectid, user__id=request.user.id)
    project.deleted=True
    project.save()

    relprojects = portmodel.relProjectPortfolio.objects.filter(project__id=project.id, deleted=False)
    if relprojects!=None and len(relprojects)>0:
        for proj in relprojects:
            proj.deleted = True
            proj.save()

    return HttpResponseRedirect('/project/')

@login_required(login_url=settings.LOGIN_URL)
def open(request, projectid):
    project = projectmodel.project.objects.get(pk=projectid, user__id=request.user.id)
    projectmedia = projectmodel.projectmedia.objects.filter(project__id=projectid)
    saved = False
    if request.method == "POST":
        form = projform.projectform(request.POST, request.FILES, instance=project)
        if form.is_valid():
            projectmdl = form.save()

            removedmedias = request.POST.getlist('removedmedia')

            for media in removedmedias:
                projectmedia = projectmodel.projectmedia.objects.get(pk=media)
                projectmedia.delete()

            if len(form.cleaned_data['projectpic'])>0:
                #medias = projectmodel.projectmedia.objects.filter(project__id=projectmdl.id)
                #for media in medias:
                #    media.delete()

                for each in form.cleaned_data['projectpic']:
                    media = projectmodel.projectmedia()
                    media.file = each
                    media.project = projectmdl
                    media.save()

            saved = True
            projectmedia = projectmodel.projectmedia.objects.filter(project__id=projectid)
            return render(request, 'project/open.html', {'request':request,'form': form,'saved':saved,
                                                    'projectid':projectid,'projectmedia':projectmedia});
        else:
            #form = projform.projectform(instance=project)
            return render(request, 'project/open.html', {'request': request, 'form': form, 'projectid': projectid
                , 'projectmedia': projectmedia});

    form = projform.projectform(instance=project)
    return render(request, 'project/open.html', {'request':request,'form': form,'projectid':projectid
                                                 ,'projectmedia':projectmedia});

@login_required(login_url=settings.LOGIN_URL)
def remmovemedia(request,mediaid):
    try:
        media = projectmodel.projectmedia.get(pk=mediaid)
        media.delete()
        return JsonResponse({ 'success' : True, 'message' : 'Deleted' })
    except Exception as ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message' : 'Media not found.'})

