from django import template
from account import models as usermodel
register = template.Library()

@register.simple_tag
def getuserprofilepic(userid):
    profile = usermodel.Userprofile.objects.get(user__id=userid)
    return '/{0}/{1}'.format('media',profile.profilepic)