from django.conf.urls import url
from project import views as projectviews

urlpatterns = [
     url(r'^new/$', projectviews.create),
     url(r'^view/(?P<projectid>[0-9]+)$', projectviews.view),
     url(r'^remove/(?P<projectid>[0-9]+)$', projectviews.remove),
     url(r'^open/(?P<projectid>[0-9]+)$', projectviews.open),

     url(r'^$', projectviews.index),
]
