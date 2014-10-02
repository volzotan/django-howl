from django.conf.urls import patterns, url

from mongodb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='mongodb'),
    url(r'^(?P<mongodb_name>\w+)/$', views.display, name='mongodb_display'),
)