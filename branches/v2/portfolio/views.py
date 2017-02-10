from django.shortcuts import render_to_response,render
from portfolio import forms as portform
from portfolio import models as portmodel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from project import models as projectmodel
import string
import random
from portfolio import dto
from django.contrib.auth.decorators import login_required
from django.conf import settings
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from account import models as accountmodel

@login_required(login_url=settings.LOGIN_URL)
def view(request, portuuid):
    portfolio = portmodel.portFolio.objects.get(user__id=request.user.id, uuid=portuuid, deleted=False)
    relprojects = portmodel.relProjectPortfolio.objects.filter(portfolio__id = portfolio.id, deleted=False)
    projects = []
    for project in relprojects:
        projects.append(projectmodel.project.objects.get(pk=project.project.id))

    profile = accountmodel.Userprofile()
    try:
        profile = accountmodel.Userprofile.objects.get(user__id=portfolio.user.id)
    except Exception as ObjectDoesNotExist:
        profile = accountmodel.Userprofile()

    return render(request, 'public/viewportfolio.html',
                              {'request':request,'projects': projects, 'portfolio': portfolio,'profile':profile });

@login_required(login_url=settings.LOGIN_URL)
def index(request):
    portfolioslist = []
    protocol = 'http'
    if request.is_secure():
        protocol = 'https'

    publicportfolios = []
    unpublicportfolios = []
    portfolios = portmodel.portFolio.objects.filter(user__id = request.user.id, deleted=False).order_by('-create_date')
    for portfolio in portfolios:
        portdto = dto.portfoliodto()
        projects = portmodel.relProjectPortfolio.objects.filter(portfolio__id = portfolio.id, deleted=False)
        portfoliodtobj = portdto.copy(portfolio)
        hitcount = HitCount.objects.get_for_object(portfolio)
        portfoliodtobj.hitcount = hitcount.hits
        portfoliodtobj.url = '{2}://{0}/public/portfolio/{1}'.format(request.META['HTTP_HOST'],
                                                                   portfoliodtobj.uuid, protocol)

        portfoliodtobj.totalprojects = len(projects)
        if portfoliodtobj.public:
            publicportfolios.append(portfoliodtobj)
        else:
            unpublicportfolios.append(portfoliodtobj)

    return render(request, 'portfolio/index.html',{'request':request,'publicportfolios':publicportfolios,
                                                      'unpublicportfolios':unpublicportfolios})

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url=settings.LOGIN_URL)
def createportfolio(request):
    projects = projectmodel.project.objects.filter(user__id=request.user.id, deleted=False)
    if request.method == 'POST':
        portfoliofrm = portform.portfolioForm(request.POST, request.FILES)
        if portfoliofrm.is_valid():
            user = User.objects.get(pk=request.user.id)
            portfoliomodel = portfoliofrm.save(commit=False)
            portfoliomodel.uuid = id_generator()
            portfoliomodel.user = user
            portfoliomodel.save()

            selectedprojects = request.POST.getlist('project')
            for project in selectedprojects:
                relmodel = portmodel.relProjectPortfolio()
                relmodel.portfolio = portfoliomodel
                relmodel.project = projectmodel.project.objects.get(pk=project)
                relmodel.save()

            return HttpResponseRedirect('/portfolio/')
        else:
            return render(request,'portfolio/create-portfolio.html', {'request':request,'form': portfoliofrm, 'projects': projects});
    else:
        portfoliofrm = portform.portfolioForm()
        return render(request,'portfolio/create-portfolio.html', {'request':request,'form': portfoliofrm, 'projects': projects});

@login_required(login_url=settings.LOGIN_URL)
def openportfolio(request, portfolioid):

    portfolio = portmodel.portFolio.objects.get(pk=portfolioid, user__id=request.user.id)
    saved = False
    if request.method == "POST":
        portfolioform = portform.portfolioForm(request.POST, request.FILES,instance=portfolio)
        portfolioform.save();

        selectedprojects = request.POST.getlist('project')

        relprojects = portmodel.relProjectPortfolio.objects.filter(portfolio__id = portfolio.id)
        for prj in relprojects:
            prj.delete()

        for project in selectedprojects:
            relmodel = portmodel.relProjectPortfolio()
            relmodel.portfolio = portfolio
            relmodel.project = projectmodel.project.objects.get(pk=project)
            relmodel.save()

        saved = True

    projects = portmodel.relProjectPortfolio.objects.filter(portfolio__id = portfolio.id, deleted=False)
    portfolioform = portform.portfolioForm(instance = portfolio)
    projectlist = []
    projectids=[]
    for project in projects:
        projectids.append(project.project.id)
        projectlist.append(project.project)

    allprojects = projectmodel.project.objects.filter(user__id=request.user.id, deleted=False)\
        .exclude(id__in=projectids)

    return render(request, 'portfolio/open-portfolio.html', {'request':request,'form': portfolioform,
                                                                'projects':projectlist,
                                                                'allprojects':allprojects,
                                                                'portfolioid' : portfolioid,'saved':saved});

@login_required(login_url=settings.LOGIN_URL)
def makepublic(request, portfolioid):
    portfoio = portmodel.portFolio.objects.get(user__id=request.user.id, pk=portfolioid)
    portfoio.public = not portfoio.public
    portfoio.save()
    return HttpResponseRedirect('/portfolio/')

@login_required(login_url=settings.LOGIN_URL)
def removeportfolio(request, portfolioid):
    portfoio = portmodel.portFolio.objects.get(user__id=request.user.id, pk=portfolioid)
    portfoio.deleted = True
    portfoio.save()
    return HttpResponseRedirect('/portfolio/')
