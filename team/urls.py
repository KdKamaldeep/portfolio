from django.conf.urls import url
from team import views as teamview

urlpatterns = [
     url(r'^$', teamview.index),
     url(r'^create_team/$', teamview.create_team),
     url(r'^new/$', teamview.create_team),
     url(r'^sendteaminvitation/(?P<teamid>[0-9,a-z,A-Z]+)/(?P<userid>[0-9]+)/$',teamview.send_team_invitation),
     url(r'^addmember/(?P<teamid>[0-9,a-z,A-Z]+)/$', teamview.addmember),
     url(r'^edit/(?P<hostedteamid>[0-9,a-z,A-Z,-]+)/$', teamview.editteam),
     url(r'^delete/(?P<teamid>[0-9,a-z,A-Z,-]+)/$', teamview.deleteteam),
     url(r'^leaveteam/(?P<teamid>[0-9,a-z,A-Z]+)/(?P<invited_userid>[0-9]+)/$', teamview.leave_team),
     url(r'^removeteaminvitation/(?P<teamid>[0-9,a-z,A-Z]+)/(?P<userid>[0-9]+)/$',teamview.remove_team_invitation),
     url(r'^view/(?P<hostedteamid>[0-9,a-z,A-Z,-]+)/(?P<sts>[0-9,a-z,A-Z]+)$', teamview.teamboard),
     url(r'^accept_reject_invitation_request/(?P<inviteduser_id>[0-9,a-z,A-Z]+)/(?P<teamid>[0-9,a-z,A-Z]+)/(?P<status>[0-9,a-z,A-Z]+)$',teamview.accept_reject_invitation_request),
     url(r'^getteams/(?P<inviteduser_id>[0-9,a-z,A-Z]+)/(?P<teamid>[0-9,a-z,A-Z]+)/$', teamview.get_teams),
     url(r'^changeteamstatus/(?P<teamid>[0-9,a-z,A-Z]+)/(?P<status>[a-z,A-Z]+)/$',teamview.change_team_status),



]

'''url(r'^teamboard/(?P<inviteduser_id>[0-9,a-z,A-Z]+)/(?P<teamid>[0-9,a-z,A-Z]+)/$', teamview.teamboard),
<a href="/team/teamboard/{{inviterequest.inviteduser.id}}/{{inviterequest.team.id}}">
'''