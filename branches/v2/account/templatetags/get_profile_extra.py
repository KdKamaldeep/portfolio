from django import template
from account.models import Userprofile, contactrequest,usercontact
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()

@register.simple_tag
def email_verified(request):
    if request.user.is_authenticated:
        try:
            userprofile = Userprofile.objects.get(user__id=request.user.id)
            if userprofile.emailverified == False:
                return "<div id='emailverifymessage' style='width: 80%;margin: 0px auto;border-radius: 0px;' class='alert alert-warning'>We need to verify your email address. We've send an email to" \
                   " <span style='    text-decoration: underline;'>"+ request.user.email +"</span> to verify your email address. Please click the link in that email to continue.</div>"
        except Exception as e:
            print e

    return ''

@register.simple_tag
def user_profile_pic(user):
    profile = Userprofile.objects.get(user__id=user.id)
    return profile_pic(profile)

@register.simple_tag
def user_profile_pic_by_id(userid):
    profile = Userprofile.objects.get(user__id=userid)
    return profile.profilepic

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
def already_contact(currentuserid, contactid):
    contacts = usercontact.objects.filter(user__id=currentuserid, contact__id=contactid)
    return contacts.count() > 0

@register.simple_tag
def request_already_sent(fromuserid, touserid):
    contactrequests = contactrequest.objects.filter(fromuser__id=fromuserid, touser__id=touserid, status='PENDING')
    return contactrequests.count() > 0

@register.simple_tag
def profile_pic(userprofile):
    if userprofile.profilepic:
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
