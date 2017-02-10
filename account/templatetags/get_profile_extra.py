from django import template
from account.models import Userprofile, contactrequest,usercontact
from django.core.exceptions import ObjectDoesNotExist
from project.models import projectmedia
from project.models import project
from portfolio.models import portFolio
from django.contrib.auth.models import User
from onlineportfolio import settings
from team import models as teammodel
import os
from django.contrib.sites.models import Site

register = template.Library()

@register.simple_tag
def email_verified(request):
    if request.user.is_authenticated:
        try:
            userprofile = Userprofile.objects.get(user__id=request.user.id)
            if userprofile.emailverified == False:
                return "<div id='emailverifymessage' style='width: 40%;border-radius: 0px;margin-left: 10%;' class='alert alert-warning'>We need to verify your email address. We've send an email to" \
                   " <span style='    text-decoration: underline;'>"+ request.user.email +"</span> to verify your email address. Please click the link in that email to continue.</div>"
        except Exception as e:
            print e

    return ''

@register.simple_tag
def user_profile_pic(user):
   # profile = Userprofile.objects.get(user__id=user.id)
   profile=get_profile(user)
   if profile!=None:
       return profile_pic(profile)
   else:
       return '/static/design/assets/img/no-Image.png'

@register.simple_tag
def user_profile_pic_by_id(userid):
    profile = Userprofile.objects.get(user__id=userid)
    return profile_pic(profile)

@register.simple_tag
def popover_position(counter):
    if counter % 2 == 0:
        return "left"

    return "right"

@register.simple_tag
def get_contact_requests(userid):
    contactrequests = contactrequest.objects.filter(touser__id=userid, status='PENDING')
    return contactrequests

@register.simple_tag
def get_profile_contacts_count(userid):
    usercontacts = usercontact.objects.filter(user__id=userid)
    return usercontacts.count()

@register.simple_tag
def get_profile(userid):
    try:
        profile = Userprofile.objects.get(user__id=userid)
        return profile
    except Exception as ObjectDoesNotExist:
        return None

@register.filter
def classname(obj):
    return obj.target.__class__.__name__

@register.simple_tag
def popover_position_3_column(counter):
    if counter % 3 == 0:
        return "left"

    return "right"


@register.simple_tag
def profile_pic(userprofile):
    if userprofile.profilepic:
        imagepath = settings.BASE_DIR + '/media/' + str(userprofile.profilepic)
        if os.path.exists(imagepath):
            return '/media/' + str(userprofile.profilepic)

    return '/static/design/assets/img/no-Image.png'

@register.simple_tag
def get_user_contacts_by_userid(userid):
    usercontacts = usercontact.objects.filter(user__id=userid)
    if usercontacts.count() > 4:
        leftcontact = (usercontacts.count() - 4)
        showncontacts = usercontacts[:4]
        return {'usercontacts' : showncontacts, 'showmore':True,
                'leftcontacts': leftcontact,'totalcontacts':usercontacts.count()}

    return {'usercontacts' : usercontacts, 'showmore':False, 'totalcontacts':usercontacts.count()}

@register.simple_tag
def get_project_pic(projectid):
    projectmedias = projectmedia.objects.filter(project__id=projectid)
    if projectmedias.count() > 0:
        return '/media/' + str(projectmedias[0].file)

    return '/static/design/assets/img/no-Image.png'

@register.simple_tag
def get_portfolio_extension_url(request):
    host = request.META['HTTP_HOST'];
    host = str(host).replace('www.','')
    return host


@register.simple_tag
def get_invitation_request(userid):
    inviterequests = teammodel.teaminvites.objects.filter(inviteduser__id=userid, status='PENDING')
    return inviterequests

@register.simple_tag
def invitation_already_sent(teamid, inviteduserid):
    teammember = teammodel.teaminvites.objects.filter(team__id=teamid, inviteduser__id=inviteduserid, deleted=False)
    return teammember.count() > 0


@register.simple_tag
def already_contact(currentuserid, contactid):
    contacts = usercontact.objects.filter(user__id=currentuserid, contact__id=contactid, deleted=False)
    return contacts.count() > 0

@register.simple_tag
def request_already_sent(fromuserid, touserid):
    contactrequests = contactrequest.objects.filter(fromuser__id=fromuserid, touser__id=touserid, status='PENDING')
    return contactrequests.count() > 0


@register.simple_tag
def already_team_member(currentuserid, teamid):
    already_accepted_team_member = teammodel.teaminvites.objects.filter(inviteduser__id=currentuserid, team__id=teamid,status='ACCEPTED');
    return already_accepted_team_member.count() > 0



@register.simple_tag
def count_team_member(teamid):
    teammembers = teammodel.teaminvites.objects.filter(team__id=teamid,deleted=False)
    if teammembers.count() > 4:
        leftmember = (teammembers.count() - 4)
        shownmember = teammembers[:4]
        return {'teammembers': shownmember, 'showmore': True,
                'leftmember': leftmember, 'totalmember': teammembers.count(),'allmembers':teammembers}

    return {'teammembers' : teammembers, 'showmore':False, 'totalmember': teammembers.count(),'allmembers':teammembers}


@register.simple_tag
def count_accepted_team_member(teamid):
    teammembers = teammodel.teaminvites.objects.filter(team__id=teamid,status="ACCEPTED")
    if teammembers.count() > 4:
        leftmember = (teammembers.count() - 4)
        shownmember = teammembers[:4]
        return {'teammembers': shownmember, 'showmore': True,
                'leftmember': leftmember, 'totalmember': teammembers.count(),'allmembers':teammembers}

    return {'teammembers' : teammembers, 'showmore':False, 'totalmember': teammembers.count(),'allmembers':teammembers}


@register.simple_tag(takes_context=True)
def addlength(context, val1, val2):
    newval = val1 + val2;
    return newval


@register.simple_tag
def count_accepted_members_projects(teamid):
    teaminvites = teammodel.teaminvites.objects.filter(team__id=teamid);

    accepted_team_membrs = [];
    for invite_members in teaminvites:
        if invite_members.status == "ACCEPTED":
            accepted_team_membrs.append(invite_members.inviteduser_id);

    totalprojects = 0;
    for memberid in accepted_team_membrs:
        count_member_projects = project.objects.filter(user__id = memberid).count();
        totalprojects += count_member_projects;

    return totalprojects;


@register.simple_tag
def count_accepted_members_portfolio(teamid):
    teaminvites = teammodel.teaminvites.objects.filter(team__id=teamid);

    accepted_team_membrs = [];
    for invite_members in teaminvites:
        if invite_members.status == "ACCEPTED":
            accepted_team_membrs.append(invite_members.inviteduser_id);


    totalportfolio = 0;
    for memberid in accepted_team_membrs:
        count_member_projects = portFolio.objects.filter(user__id = memberid).count();
        totalportfolio += count_member_projects;

    return totalportfolio;


@register.simple_tag
def get_owner_id_by_teamid(teamid):
    owner = teammodel.team.objects.get(pk=teamid);
    return User.objects.get(pk=owner.owner_id);
    #return owner.owner_id;


@register.simple_tag
def getcurrentdomain(request):
    django_site = Site.objects.get_current()
    return request.META['HTTP_HOST'];


@register.simple_tag
def getprojectimagebyprojectid(projectid):
    prjimgpath = projectmedia.objects.get(project__id=projectid);
    return prjimgpath;

