from django.conf.urls import patterns, url

from forecast import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='forecast'),
)