from django.shortcuts import render,render_to_response
from portfolio import models as portmodel
from project import models as projectmodel
from django.http import Http404
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib.auth.models import User
from account import models as Userprofile
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from notifications.signals import notify
from account.models import  contactrequest, usercontact
from django.contrib.auth.decorators import login_required
from django.conf import settings

def portfolio(request, portuuid):

    try:
        portfolio = portmodel.portFolio.objects.get(uuid=portuuid, deleted=False, public=True)
        relprojects = portmodel.relProjectPortfolio.objects.filter(portfolio__id=portfolio.id, deleted=False)
        projects = []
        for project in relprojects:
            projects.append(projectmodel.project.objects.get(pk=project.project.id))

        if request.user.id != portfolio.user.id:
            hit_count = HitCount.objects.get_for_object(portfolio)
            hit_count_response = HitCountMixin.hit_count(request, hit_count)

        profile = Userprofile.Userprofile()
        try:
            profile = Userprofile.Userprofile.objects.get(user__id=portfolio.user.id)
        except Exception as ObjectDoesNotExist:
            profile = Userprofile.Userprofile()

        return render_to_response('public/viewportfolio.html', RequestContext(request, {'request':request,'projects': projects,
                                                                                        'portfolio': portfolio,'profile':profile}));

    except Exception as ObjectDoesNotExist:
        raise Http404

def project(request, portuuid, projectid):
    try:
        portfolio = portmodel.portFolio.objects.get(uuid=portuuid, deleted=False, public=True)

        if portfolio == None:
            raise Http404

    except Exception as ObjectDoesNotExist:
        raise Http404

    project = projectmodel.project.objects.select_related('user').get(pk = projectid, deleted=False)
    services = project.services.split(',')
    profile = Userprofile.Userprofile()
    try:
        profile = Userprofile.Userprofile.objects.get(user__id=project.user.id)
    except Exception as ObjectDoesNotExist:
        profile = Userprofile.Userprofile()

    return render(request, 'public/viewproject.html', {'project': project,'userprofile':profile,'services':services})

@login_required(login_url=settings.LOGIN_URL)
def send_contact_request(request, touserid):

    if touserid == request.user.id:
        # You can't send contact requet to yourself.
        return JsonResponse({'success': True})

    cntrequest = contactrequest.objects.filter(fromuser__id=request.user.id, touser__id=touserid, status='PENDING')
    if cntrequest.count() > 0:
        return JsonResponse({'success': True})

    contrequest = contactrequest()
    contrequest.fromuser = User.objects.get(pk=request.user.id)
    contrequest.touser = User.objects.get(pk=touserid)
    contrequest.save()
    notifieduser = User.objects.get(pk=touserid)

    notify.send(request.user, recipient=notifieduser,
                verb='{0} {1} send you a contact request'.format(request.user.first_name,
                                                                 request.user.last_name), target=contrequest)

    notify.send(request.user, recipient=request.user,
                verb='You have sent a Contact Request to {0} {1}'.format(notifieduser.first_name,
                                                                       notifieduser.last_name), target=contrequest)

    return JsonResponse({'success': True})

@login_required(login_url=settings.LOGIN_URL)
def mark_as_read(request):
    request.user.notifications.mark_all_as_read()
    return JsonResponse({'success':True})

@login_required(login_url=settings.LOGIN_URL)
def accept_reject_contact_request(request, contactrequestid, status):
    cntactrequest = contactrequest.objects.get(pk=contactrequestid)
    if cntactrequest != None:
        cntactrequest.status = status
        cntactrequest.save()

        if status == "ACCEPTED":
            usercntact = usercontact()
            usercntact.user = request.user
            usercntact.contact = cntactrequest.fromuser
            usercntact.save()

            notify.send(request.user, recipient=cntactrequest.fromuser,
                        verb='{0} {1} accepted your contact request'.format(request.user.first_name,
                                                                            request.user.last_name))

            usercntactreverse = usercontact()
            usercntactreverse.user = cntactrequest.fromuser
            usercntactreverse.contact = request.user
            usercntactreverse.save()

            notify.send(request.user, recipient=request.user,
                        verb='You have accepted contact request from {0} {1}'
                        .format(cntactrequest.fromuser.first_name, cntactrequest.fromuser.last_name))

    return JsonResponse({'success': True})

def viewprofile(request,userid, full):
    user = User.objects.get(pk=userid)

    contactrequestsent = 'NOTSENT'
    contactexist = False
    showacceptrejectbutton = False
    showrequestbutton = True
    cntactrequest = None

    usercntct = usercontact.objects.filter(user__id=request.user.id, contact__id=user.id)
    if usercntct.count() > 0:
        contactrequestsent = 'ALREADYACONTACT'
        contactexist = True

    if contactexist == False:
        contactrequests = contactrequest.objects.filter(fromuser__id=request.user.id, touser__id=userid, status='PENDING')
        if contactrequests.count() > 0:
            contactrequestsent = 'SENT'

        contactrequestmodes = contactrequest.objects.filter(touser__id=request.user.id, fromuser__id=userid, status='PENDING')

        if contactrequestmodes.count() > 0:
            showacceptrejectbutton = True
            showrequestbutton = False
            cntactrequest = contactrequestmodes[0]

    userprofile = Userprofile.Userprofile.objects.get(user__id=user.id)

    template = "public/viewprofile-popup.html"
    if full == "yes":
        template = "public/viewprofile-full.html"

    return render(request, template,
                              {'userprofile':userprofile,
                               'user':user,'contactrequestsent':contactrequestsent,
                               'showrequestbutton':showrequestbutton,
                               'showacceptrejectbutton':showacceptrejectbutton,
                               'contactrequest':cntactrequest});

def searchprojects(request):
    projects = portmodel.relProjectPortfolio.objects.order_by('project__id').distinct('project__id')\
        .filter(project__deleted=False, portfolio__deleted=False,portfolio__public=True)
    name = ""
    services = ""
    startdate = ""
    enddate = ""
    url = ""

    if 'name' in request.GET:
        name = request.GET['name']
        if name != "":
            projects = projects.filter(project__title__icontains=name)

    if 'services' in request.GET:
        services = request.GET['services']
        if services != "":
            projects = projects.filter(project__services__icontains=services)

    if 'url' in request.GET:
        url = request.GET['url']
        if url != "":
            projects = projects.filter(project__url__icontains=url)

    paginator = Paginator(projects, 10)

    page = request.GET.get('page')
    try:
        projectlist = paginator.page(page)
    except PageNotAnInteger:
        projectlist = paginator.page(1)
    except EmptyPage:
        projectlist = paginator.page(paginator.num_pages)

    return render(request, 'public/searchprojects.html', {'projects': projectlist,'name':name,'services':services,
                                                  'startdate':startdate,'enddate':enddate,
                                                  'url':url})

def searchportfolios(request):
    portfolios = portmodel.portFolio.objects.filter(deleted=False,public=True)

    title = request.GET.get('title')
    if title != None and title != '':
        portfolios = portfolios.filter(title__icontains=title)
    else:
        title=""

    paginator = Paginator(portfolios, 10)

    page = request.GET.get('page')
    try:
        portfoliolist = paginator.page(page)
    except PageNotAnInteger:
        portfoliolist = paginator.page(1)
    except EmptyPage:
        portfoliolist = paginator.page(paginator.num_pages)

    return render(request, 'public/searchportfolios.html', {'portfolios': portfoliolist, 'title': title})

def searchcontacts(request):

    if request.user.is_authenticated:
        userprofiles = Userprofile.Userprofile.objects.filter(deleted=False, emailverified=True).exclude(
            user__id=request.user.id) \
            .order_by('-create_date')
    else:
        userprofiles = Userprofile.Userprofile.objects.filter(deleted=False, emailverified=True)\
        .order_by('-create_date')

    firstname = request.GET.get('first_name') or ''
    lastname = request.GET.get('last_name') or ''
    email = request.GET.get('email') or ''

    if firstname != None and firstname != '':
        userprofiles = userprofiles.filter(user__first_name__icontains=firstname)

    if lastname != None and lastname != '':
        userprofiles = userprofiles.filter(user__last_name__icontains=lastname)

    if email != None and email != '':
        userprofiles = userprofiles.filter(user__email=email)

    paginator = Paginator(userprofiles, 12)

    page = request.GET.get('page')
    try:
        userprofileslist = paginator.page(page)
    except PageNotAnInteger:
        userprofileslist = paginator.page(1)
    except EmptyPage:
        userprofileslist = paginator.page(paginator.num_pages)

    return render(request, 'public/searchcontacts.html', {'userprofiles' :
                                                              userprofileslist,'first_name':firstname
                                                          ,'last_name':lastname,'email':email})
