from django.conf.urls import patterns, url

from howlcore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='main_page'),
    url(r'^settings/$', views.display, name='howlcore'),
    url(r'^settings/logging/$', views.logging, name='howlcore_logging'),
    url(r'^settings/celery/$', views.celery, name='howlcore_celery'),
)