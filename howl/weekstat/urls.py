from django.conf.urls import patterns, url

from weekstat import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='weekstat'),

    url(r'^(?P<weekstat_name>\w+)/$', views.display, name='weekstat_display'),
    url(r'^(?P<weekstat_name>\w+)/rawdata/$', views.rawdata, name='weekstat_rawdata'),
)