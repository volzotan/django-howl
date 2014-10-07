from django.conf.urls import patterns, url

from rule import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='rule'),

    # ex: /rule/name/
    url(r'^(?P<rule_name>\w+)/$', views.display, name='rule_display'),

    url(r'^(?P<rule_name>\w+)/test/$', views.test, name='rule_test'),
    url(r'^(?P<rule_name>\w+)/trigger/$', views.trigger, name='rule_trigger'),
)