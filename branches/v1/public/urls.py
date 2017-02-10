from django.conf.urls import url
from public import views as pubviews

urlpatterns = [
     url(r'^portfolio/(?P<portuuid>[0-9,a-z,A-Z]+)$', pubviews.portfolio),
     url(r'^project/(?P<portuuid>[0-9,a-z,A-Z]+)/(?P<projectid>[0-9]+)$', pubviews.project),
     url(r'^searchprojects/$', pubviews.searchprojects),
     url(r'^searchportfolios/$', pubviews.searchportfolios),
     url(r'^viewprofile/(?P<userid>[0-9,a-z,A-Z]+)/(?P<full>[0-9,a-z,A-Z]+)$', pubviews.viewprofile),
     url(r'^mark_as_read/$', pubviews.mark_as_read),
     url(r'^accept_reject_contact_request/(?P<contactrequestid>[0-9,a-z,A-Z]+)/(?P<status>[0-9,a-z,A-Z]+)$',
         pubviews.accept_reject_contact_request),
     url(r'^send_contact_request/(?P<touserid>[0-9,a-z,A-Z]+)/(?P<fromuserid>[0-9,a-z,A-Z]+)$',
         pubviews.send_contact_request)
     ]