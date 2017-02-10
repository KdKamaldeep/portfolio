from django.conf.urls import url
from portfolio import views as portviews

urlpatterns = [
     url(r'^new/$', portviews.createportfolio),
     url(r'^view/(?P<portuuid>[0-9,a-z,A-Z]+)$', portviews.view),
     url(r'^$', portviews.index),
     url(r'^open/(?P<portfolioid>[0-9]+)$', portviews.openportfolio),
     url(r'^makepublic/(?P<portfolioid>[0-9]+)$', portviews.makepublic),
     url(r'^removeportfolio/(?P<portfolioid>[0-9]+)$', portviews.removeportfolio),
     url(r'^viewportfolio/(?P<portfolioid>[0-9,a-z,A-Z]+)$', portviews.viewportfolio)
]
