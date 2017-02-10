import uuid
import json
from django.http import  JsonResponse
from forms import userform as user

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from account import forms as accountform
from common import emailhelper
from django.core.signing import Signer
from .forms import profileform
from .models import Userprofile, usercontact
from public.views import send_contact_request

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

            # Send contact request is user opted too.
            if 'contactrequestid' in request.session:
                send_contact_request(request, request.session['contactrequestid'])
                del request.session['contactrequestid']
                request.session.modified = True

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

    if 'cnt' in request.GET:
        cnt = request.GET['cnt']  # User id where contact request should be sent.
        request.session['contactrequestid'] = cnt

    if request.method == 'POST':
        try:
            userfrm = accountform.userform(request.POST)
            user = User.objects.create_user(request.POST['username'], request.POST['emailaddress'], request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name= request.POST['last_name']
            user.save()

            userprofile = Userprofile()
            userprofile.user = user
            userprofile.membertype = request.POST['membertype']
            userprofile.position = request.POST['position']
            userprofile.save()

            login(request, user)

            emailhelper.send_verification_email(user)
            emailhelper.send_welcome_email(user)

            # Send contact request is user opted too.
            if 'contactrequestid' in request.session:
                send_contact_request(request, request.session['contactrequestid'])
                del request.session['contactrequestid']
                request.session.modified = True

            return HttpResponseRedirect('/account/editprofile')
        except Exception as e:
            raise e
            #return render(request,'account/signup.html', {'request':request,'form':userfrm});
    else:
        userfrm = accountform.userform()
        return render(request, 'account/signup.html', {'request': request, 'form': userfrm});

def signout(request):
    logout(request)
    return HttpResponseRedirect('/account/signin')

def handleuploadfile(file):

    filename = "%s.%s" % (uuid.uuid4(), '.jpg')
    path = 'profile/{0}'.format(filename)
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
        profile.skypeid = request.POST['skypeid']
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
        return HttpResponseRedirect('/account/profile/')
        #return render(request, 'account/editprofile.html', {'saved': saved, 'form': userfrm,'proform':proform});
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

    if 'newpassword' in request.POST:
        oldpassword = request.POST.get('oldpassword').strip()
        newpassword= request.POST['newpassword'].strip()
        confirmpassword = request.POST['confirmpassword'].strip()

        saveuser = User.objects.get(pk=request.user.id)

        if saveuser.check_password(oldpassword):
            saveuser.set_password(request.POST['newpassword']);
            saveuser.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        return HttpResponseRedirect('/account/profile/')



@login_required(login_url=settings.LOGIN_URL)
def contacts(request):
    usercontacts = usercontact.objects.filter(user__id=request.user.id,deleted=False)
    user = User.objects.get(pk=request.user.id)
    userprofile = Userprofile.objects.get(user__id=user.id)

    return render(request,'account/contacts.html', {'userprofile':userprofile,'user':user, 'usercontacts':usercontacts})


@login_required(login_url=settings.LOGIN_URL)
def removecontact(request, contactid):
    contact = usercontact.objects.get(contact__id=contactid, user__id=request.user.id)
    othercontact = usercontact.objects.get(contact__id = request.user.id, user__id=contactid)

    if contact != None and othercontact !=None:
        contact.deleted = True;
        othercontact.deleted = True
        contact.save();
        othercontact.save();

    return HttpResponseRedirect('/account/contacts/')


'''@login_required(login_url=settings.LOGIN_URL)
def removecontact(request, contactid):
    contact = usercontact.objects.get(pk=contactid, user__id=request.user.id)
    othercontact = usercontact.objects.get(contact__id = request.user.id, user__id=contact.contact.id)
    if contact != None:
        contact.delete()
        othercontact.delete()

    return HttpResponseRedirect('/account/contacts/')'''

def verifyemail(request):
    signer = Signer()
    userid = request.GET.get('id')
    useridclear = signer.unsign(userid)
    userprofile = Userprofile.objects.get(user__id=useridclear)
    userprofile.emailverified = True
    userprofile.save()
    return render(request,'account/email-verified.html',{})