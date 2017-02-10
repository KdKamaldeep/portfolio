from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from account.models import Userprofile
from django.core.exceptions import ObjectDoesNotExist
def index(request):
    try:
        user = User.objects.get(username__iexact=request.subdomain)
        userprofile = None
        if user != None:
            userprofile = Userprofile.objects.get(user__id=user.id)
        return render(request, 'home/user-home.html', {'user': user,'userprofile':userprofile });
    except Exception as ObjectDoesNotExist:
        return render(request, 'home/index.html');