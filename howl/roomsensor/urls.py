from django.conf.urls import patterns, url

from roomsensor import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='roomsensor'),

    # ex: /roomsensor/name/
    url(r'^(?P<roomsensor_name>\w+)/$', views.display, name='roomsensor_display'),
    url(r'^(?P<roomsensor_name>\w+)/read/$', views.read, name='roomsensor_read'),

    # JSON data for graph creation
    url(r'^(?P<roomsensor_name>\w+)/rawdata/(?P<datapoints>\d+)/(?P<compression_factor>\d+)/$', views.rawdata, name='roomsensor_rawdata'),
)