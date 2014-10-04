from django.conf.urls import patterns, url

from relay import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='relay'),

    url(r'^(?P<relay_name>\w+)/$', views.display, name='relay_display'),
    url(r'^(?P<relay_name>\w+)/switch/(?P<switch>\w+)/$', views.switch, name='relay_switch'),
)