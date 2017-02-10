from django.shortcuts import render_to_response,render
from account import forms as accountform
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Userprofile, usercontact
from .forms import profileform
import uuid
from emailhelper import sendverificationemail
from notifications.signals import notify


def signin(request):
    loginfrm = accountform.loginform()

    next = '/portfolio/'

    if 'next' in request.GET:
        next = request.GET['next']

    if 'cnt' in request.GET:
        cnt = request.GET['cnt'] # User id where contact request should be sent.
        request.session['contactrequestid'] = cnt

    if request.method == 'POST':
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user != None:
            login(request, user)

            '''if 'contactrequestid' in request.session:

                notifieduser = User.objects.get(pk=request.session['contactrequestid'])
                notify.send(request.user, recipient=notifieduser,
                            verb='{0} {1} have sent you a contact request'.format(request.user.first_name,
                                                                                  request.user.last_name))
                del request.session['contactrequestid']
                request.session.modified = True'''

            if 'next' in request.POST:
                nexturl = request.POST['next']
            else:
                nexturl = next

            return HttpResponseRedirect(nexturl)
        else:
            return render(request, 'account/signin.html', {'form': loginfrm, 'message': 'Invalid username/password.','next':next});

    else:
        return render(request, 'account/signin.html', {'form':loginfrm, 'message': '','next':next});

def signup(request):
    if request.method == 'POST':
        try:
            userfrm = accountform.userform(request.POST)
            user = User.objects.create_user(request.POST['username'], request.POST['emailaddress'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name= request.POST['last_name']
            user.save()


            userprofile = Userprofile()
            userprofile.user = user
            userprofile.position = request.POST['position']
            userprofile.save()

            #sendverificationemail(user)
            login(request, user)
            return HttpResponseRedirect('/portfolio/')
        except Exception as e:
            return render(request,'account/signup.html', {'request':request,'form':userfrm});
    else:
        userfrm = accountform.userform()
        return render(request, 'account/signup.html', {'request': request, 'form': userfrm});

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

def handleuploadfile(file):

    filename = "%s.%s" % (uuid.uuid4(), '.jpg')
    path = 'profile/{0}.jpg'.format(filename)
    with open('media/' + path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path

@login_required(login_url=settings.LOGIN_URL)
def editprofile(request):
    saved=False
    user = User.objects.get(pk=request.user.id)
    userfrm = accountform.userform(instance=user)

    try:
        profile = Userprofile.objects.get(user__id=user.id)
    except Userprofile.DoesNotExist:
        profile = Userprofile()

    proform = profileform(instance=profile)

    if request.method=="POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile.user = user
        profile.address = request.POST['address']
        profile.mobileno = request.POST['mobileno']
        profile.phoneno = request.POST['phoneno']
        profile.ext = request.POST['ext']
        profile.skills = request.POST['skills']
        profile.position = request.POST['position']
        if len(request.FILES)>0:
            profile.profilepic = handleuploadfile(request.FILES['profilepic'])

        profile.aboutme = request.POST['aboutme']
        profile.save()

        saved = True
        profile = Userprofile.objects.get(user__id=user.id)
        proform = profileform(instance=profile)
        user = User.objects.get(pk=request.user.id)
        userfrm = accountform.userform(instance=user)

        return render(request, 'account/editprofile.html', {'saved': saved, 'form': userfrm,'proform':proform});
    else:
        userfrm = accountform.userform(instance=user)
        return render(request, 'account/editprofile.html', {'saved': saved, 'form': userfrm, 'proform': proform});

@login_required(login_url=settings.LOGIN_URL)
def profile(request):
    user = User.objects.get(pk=request.user.id)

    userprofile = Userprofile.objects.get(user__id=user.id)

    return render(request, 'account/profile.html',
                              {'userprofile':userprofile,'user':user});

@login_required(login_url=settings.LOGIN_URL)
def changepassword(request):
    return HttpResponseRedirect('profile')

@login_required(login_url=settings.LOGIN_URL)
def contacts(request):
    usercontacts = usercontact.objects.filter(user__id=request.user.id)
    user = User.objects.get(pk=request.user.id)
    userprofile = Userprofile.objects.get(user__id=user.id)
    return render(request,'account/contacts.html', {'userprofile':userprofile,'user':user, 'usercontacts':usercontacts})


