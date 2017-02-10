from django import template
from account.models import Userprofile, contactrequest,usercontact

register = template.Library()

@register.simple_tag
def email_verified(request):
    if request.user.is_authenticated:
        userprofile = Userprofile.objects.get(user__id=request.user.id)
        if userprofile.emailverified == False:
            return "<div id='emailverifymessage' style='width: 80%;margin: 0px auto;border-radius: 0px;' class='alert alert-warning'>We need to verify your email address. We've send an email to" \
                   " <span style='    text-decoration: underline;'>"+ request.user.email +"</span> to verify your email address. Please click the link in that email to continue.</div>"

    return ''

@register.simple_tag
def user_profile_pic(user):
    profile = Userprofile.objects.get(user__id=user.id)
    return profile.profilepic

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
    profile = Userprofile.objects.get(pk=userid)
    return profile

@register.filter
def classname(obj):
    return obj.target.__class__.__name__