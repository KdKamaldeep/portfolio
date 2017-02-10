from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from account.models import Userprofile
from portfolio.models import portFolio,relProjectPortfolio
from django.core.exceptions import ObjectDoesNotExist
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from onlineportfolio import settings
from urlparse import urlparse
import os
from django.contrib.sites.models import Site

def index(request):

    django_site = Site.objects.get_current()

    print django_site.domain;

    currentdomain ="http://"+request.META['HTTP_HOST'];
    currentdomain = urlparse(str(currentdomain)).hostname

    print django_site.domain;
    print currentdomain;


    if currentdomain == django_site.domain:

        print "A"

        try:
            profiledir = settings.BASE_DIR + "/media/profile/"
            portfoliodir = settings.BASE_DIR + "/media/portfolio/"
            projectdir = settings.BASE_DIR + "/media/project/"


            if not os.path.isdir(profiledir):
                os.makedirs(profiledir)

            if not os.path.isdir(portfoliodir):
                os.makedirs(portfoliodir)

            if not os.path.isdir(projectdir):
                os.makedirs(projectdir)

        except Exception as e:
            print e

        try:
            '''user = User.objects.get(username__iexact=request.subdomain)
            userprofile = None
            if user != None:
                userprofile = Userprofile.objects.get(user__id=user.id)
                portfolio = portFolio.objects.filter(user__id=user.id,deleted=False,public=True).first()
                portfolioprojects = []

            if portfolio != None:
                portfolioprojects = relProjectPortfolio.objects.filter(portfolio__user__id=user.id,
                                                                   portfolio__deleted=False,
                                                                   portfolio__public=True, portfolio__id=portfolio.id)'''

            portfolio = portFolio.objects.get(portfolio_url__iexact=request.subdomain,deleted=False,public=True)
            user = portfolio.user
            userprofile = Userprofile.objects.get(user__id=user.id)
            portfolioprojects = []

            if portfolio != None:
                portfolioprojects = relProjectPortfolio.objects.filter(portfolio__id=portfolio.id)

            hit_count = HitCount.objects.get_for_object(portfolio)
            HitCountMixin.hit_count(request, hit_count)

            return render(request, 'home/user-home.html', {'user': user,'userprofile':userprofile,
                                                       'portfolioprojects':portfolioprojects,'portfolio':portfolio });
        except Exception as e:
            return render(request, 'home/index.html');

    else:
        subdomain = currentdomain.split('.')[0];
        portfolio = portFolio.objects.get(portfolio_url__iexact=subdomain, deleted=False, public=True)
        user = portfolio.user
        userprofile = Userprofile.objects.get(user__id=user.id)

        portfolioprojects = []

        if portfolio != None:
            portfolioprojects = relProjectPortfolio.objects.filter(portfolio__id=portfolio.id)

        hit_count = HitCount.objects.get_for_object(portfolio)
        HitCountMixin.hit_count(request, hit_count)

        return render(request, 'base/'+portfolio.portfolio_template, {'user': user,'userprofile':userprofile,
                                                                      'portfolioprojects': portfolioprojects,
                                                                      'portfolio': portfolio});

        #return render(request, 'home/user-home.html', {'user': user, 'userprofile': userprofile,
        #                                               'portfolioprojects': portfolioprojects, 'portfolio': portfolio});


def previewtemplate(request,templatename):
    return render(request, 'base/' +templatename , {});