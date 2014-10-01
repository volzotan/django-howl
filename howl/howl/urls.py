from django.conf.urls import patterns, include, url
from django.contrib import admin

from howlcore import core

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', include('howlcore.urls')),
    url(r'^core/', include('howlcore.urls'))
)

core.init()