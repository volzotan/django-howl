from django.conf.urls import patterns, url

from inkdisplay import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='inkdisplay'),

    url(r'^(?P<inkdisplay_name>\w+)/$', views.display, name='inkdisplay_display'),
)