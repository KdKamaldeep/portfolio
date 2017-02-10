from django.conf.urls import url
from account import views as accountview

urlpatterns = [
     url(r'^signin/$', accountview.signin),
     #url(r'^signin/(?P<next>[a-z])$', accountview.signin),
     url(r'^signup/$', accountview.signup),
     url(r'^signout/$', accountview.signout),
     url(r'^editprofile/$', accountview.editprofile),
     url(r'^profile/$', accountview.profile),
     url(r'^contacts/$', accountview.contacts),
     url(r'^removecontact/(?P<contactid>[0-9,a-z,A-Z]+)$', accountview.removecontact),
     url(r'^changepassword/$', accountview.changepassword),
     url(r'^verifyemail/$', accountview.verifyemail)

]
