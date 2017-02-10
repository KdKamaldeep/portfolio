from django.shortcuts import render,HttpResponseRedirect
from account import models as usermodel
from account import forms as accountform
from team import forms as teamform
from team import models as teammodel
from account import models as usermodel
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import  contactrequest, usercontact
from django.contrib.auth.models import User
from notifications.signals import notify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common import emailhelper

# Create your views here.
#def newteam(request):
   # return render(request, 'team/team.html',
    #             {});
def create_team(request):
    if request.method == 'POST':
        #if 'teamname' in request.POST:
        if teammodel.team.objects.filter(teamname=request.POST['teamname']).exists():
            return JsonResponse({'success': False, 'message': 'TeamName Already Exists.'})
        teamname = request.POST['teamname']
        aboutteam = request.POST['aboutteam']
        hostedteamid =request.POST['hostedteamid'];
        response_data = {}
        team = teammodel.team(teamname=teamname, aboutteam=aboutteam, hostedteamid = hostedteamid, owner_id=request.user.id)
        team.save()
        return HttpResponseRedirect('/team/addmember/' + str(team.id))

        #return render(request, 'team/addmember.html',
         #                 {'teamid':team.id});
        #return HttpResponseRedirect('/team/addmember/'+ str(team.id))
        #return JsonResponse({'team_id': team.id, 'success': True})
       #return JsonResponse({'success': False})
    else:
        return render(request, 'team/team.html',
                      {});

def send_team_invitation(request, teamid, userid):
    if teammodel.teaminvites.objects.filter(team__id=teamid, inviteduser__id=userid).exists():
        teminvitation = teammodel.teaminvites.objects.get(team__id=teamid, inviteduser__id=userid)
        teminvitation.team_id = teamid
        teminvitation.inviteduser_id = userid;
        teminvitation.deleted = False;
        teminvitation.status = "PENDING";
        teminvitation.save();

        return JsonResponse({'success': False,'message' : 'Already a member.'})

    teminvitation = teammodel.teaminvites()
    teminvitation.team_id = teamid
    teminvitation.inviteduser_id=userid;
    teminvitation.save();

    notifieduser=User.objects.get(id=teminvitation.inviteduser_id);

    notify.send(request.user, recipient=notifieduser,
                verb='{0} {1} send you a team invitation request'.format(request.user.first_name,
                                                                 request.user.last_name), target=teminvitation)

    notify.send(request.user, recipient=request.user,
                verb='You have sent a team invitation request to {0} {1}'.format(notifieduser.first_name,
                                                                         notifieduser.last_name), target=teminvitation)

    return JsonResponse({'success': True})

def remove_team_invitation(request, teamid, userid):
    if teammodel.teaminvites.objects.filter(team__id=teamid, inviteduser__id=userid).exists():
        teminvitation = teammodel.teaminvites.objects.get(team__id=teamid, inviteduser__id=userid)
        teminvitation.team_id = teamid
        teminvitation.inviteduser_id = userid;
        teminvitation.deleted = True;
        teminvitation.status = "PENDING";
        teminvitation.save();


        notifieduser=User.objects.get(id=teminvitation.inviteduser_id);

        notify.send(request.user, recipient=notifieduser,
                verb='{0} {1} remove from a team invitation request'.format(request.user.first_name,
                                                                 request.user.last_name), target=teminvitation)

        notify.send(request.user, recipient=request.user,
                verb='You have remove a team invitation request to {0} {1}'.format(notifieduser.first_name,
                                                                         notifieduser.last_name), target=teminvitation)

        return JsonResponse({'success': True})

def index(request):
    '''userlist = [];
    teamlist = [];
    team = teammodel.team.objects.get(userid = request.user.id)
    teamname = team.teamname;
    invitedusers = teammodel.teaminvites.objects.get(teamid = team.id);
    users=User.objects.get(id=invitedusers.userid)
    userlist.append(users);
    userbyteam = {'teamname': teamname, 'userlist': userlist}
    teamlist.append(userbyteam);
    return render(request, 'team/team.html',
              {'teamlist': teamlist});'''

    checkmembertype = usermodel.Userprofile.objects.get(user__id=request.user.id);
    teamname = request.GET.get('teamname') or ''
    sts = "";

    if checkmembertype.membertype == 'INDIVIDUAL':
        teams=[];
        sts="yes";
        if teamname != None and teamname != '':
            teamlist = teammodel.teaminvites.objects.filter(Q(inviteduser__id=request.user.id,
                                                              status='ACCEPTED',team__teamname__icontains=teamname,deleted=False));
        else:
            teamlist = teammodel.teaminvites.objects.filter(inviteduser__id=request.user.id, status='ACCEPTED',deleted=False);

        for teamlst in teamlist:
            if teamlst.team.status == 'ACTIVE':
                team = teammodel.team();
                team.id = teamlst.team.id
                team.teamname = teamlst.team.teamname;
                team.aboutteam = teamlst.team.aboutteam
                team.hostedteamid = teamlst.team.hostedteamid
                teams.append(team)

    else:
        sts= "no";
        if teamname != None and teamname != '':
            teams = teammodel.team.objects.filter(Q(owner__id=request.user.id, deleted=False, teamname__icontains=teamname))
        else:
            teams = teammodel.team.objects.filter(owner__id=request.user.id,deleted=False)


    paginator = Paginator(teams, 10)
    page = request.GET.get('page')
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)


    return render(request, 'team/index.html',
                  {'inviteduser_id': request.user.id, 'teams': teams,'teamname':teamname,'sts':sts});

def addmember(request,teamid):
    if request.user.is_authenticated:
        userprofiles = usermodel.Userprofile.objects.filter(deleted=False, emailverified=True,membertype='INDIVIDUAL').exclude(
            user__id=request.user.id) \
            .order_by('-create_date')
    else:
        userprofiles = usermodel.Userprofile.objects.filter(deleted=False, emailverified=True,membertype='INDIVIDUAL') \
            .order_by('-create_date')

    firstname = request.GET.get('first_name') or ''

    if firstname != None and firstname != '':
        userprofiles = userprofiles.filter(Q(user__first_name__icontains=firstname)
                                           | Q(user__last_name__icontains=firstname)
                                           | Q(user__email__icontains=firstname))

    paginator = Paginator(userprofiles, 12)

    page = request.GET.get('page')
    try:
        userprofileslist = paginator.page(page)
    except PageNotAnInteger:
        userprofileslist = paginator.page(1)
    except EmptyPage:
        userprofileslist = paginator.page(paginator.num_pages)

    return render(request, 'team/addmembers.html',
                 {'userprofiles': userprofileslist, 'teamid':teamid});

def teamboard(request,hostedteamid,sts):
    team = teammodel.team.objects.get(hostedteamid=hostedteamid);
    teaminvitation = teammodel.teaminvites.objects.filter(team__id=team.id, deleted=False);

    '''return render(request, 'team/teams-board.html',
                  { 'team':team,'teaminvitation':teaminvitation,'inviteduser_id':inviteduser_id});'''

    return render(request, 'team/teams-board.html',
                  {'team': team, 'teaminvitation': teaminvitation, 'inviteduser_id': request.user.id, 'sts': sts});

    '''teaminvitation = teammodel.teaminvites.objects.filter(team__id=teamid, deleted=False, );
    return render(request,'team/teams-board.html',
                  {'inviteduser_id':inviteduser_id,
                   'teamid':teamid,
                   'teaminvitation':teaminvitation});'''

def accept_reject_invitation_request(request,inviteduser_id, teamid,status):
    teaminvitation = teammodel.teaminvites.objects.filter(team__id = teamid,deleted=False);
    current_user_invitation = teammodel.teaminvites.objects.get(inviteduser__id=inviteduser_id, team__id =teamid);

    if status == 'accept':
        current_user_invitation.status = 'ACCEPTED';
    if status == 'reject':
        current_user_invitation.status = 'REJECTED';
        current_user_invitation.deleted = True;

    current_user_invitation.save();

    return HttpResponseRedirect('/team/')
    #return render(request, 'team/myteams.html',{'inviteduser_id':inviteduser_id,'teamid':teamid,'teaminvitation':teaminvitation,'status':status});

def get_teams(request,inviteduser_id,teamid):
    teamlist = teammodel.teaminvites.objects.filter(inviteduser_id=inviteduser_id, status='ACCEPTED');
    return render(request, 'team/getteams.html',{'inviteduser_id':inviteduser_id,'teamlist':teamlist});

def change_team_status(request,teamid,status):
    team = teammodel.team.objects.get(pk=teamid);
    team.status = status;
    team.save();

    teaminvitation = teammodel.teaminvites.objects.filter(team__id=teamid, deleted=False);

    sender = User.objects.get(id=team.owner_id);

    for teaminvite in teaminvitation:
        notifieduser = User.objects.get(id=teaminvite.inviteduser_id);
        notify.send(request.user, recipient=notifieduser,verb='{0} {1} marks {2} {3} '.format(request.user.first_name,
                                                request.user.last_name, team.teamname,status),target=notifieduser)

        emailhelper.change_status_email(sender=sender,teamname=team.teamname,recipient=notifieduser)


    return HttpResponseRedirect('/team/')

def editteam(request,hostedteamid):

    team = teammodel.team.objects.get(hostedteamid=hostedteamid);

    if request.method == 'POST':
        team.teamname = request.POST['teamname']
        team.aboutteam = request.POST['aboutteam']
        team.save()
        return HttpResponseRedirect('/team/addmember/' + str(team.id))

    return render(request,'team/edit-team.html',{'team':team});


def deleteteam(request,teamid):
    team = teammodel.team.objects.get(pk=teamid);
    team.deleted=True;
    team.save()

    return index(request)


def leave_team(request,teamid,invited_userid):
    teaminvitation = teammodel.teaminvites.objects.get(team__id=teamid, inviteduser__id=invited_userid);
    teaminvitation.delete();

    team = teammodel.team.objects.get(pk=teamid);
    notifieduser = User.objects.get(id=team.owner_id);

    notify.send(request.user, recipient=notifieduser,
                verb='{0} {1} left from  {2} team'.format(request.user.first_name,
                                                        request.user.last_name,team.teamname),
                                                        target=teaminvitation)

    notify.send(request.user, recipient=request.user,
                verb='You left from {0} team'.format(team.teamname),target=teaminvitation)

    return HttpResponseRedirect("/team");