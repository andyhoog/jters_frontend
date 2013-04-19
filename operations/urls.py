# -*- encoding: utf-8 -*-

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import *
from operations.views import company_leads, download_leads
urlpatterns = patterns('',
                       url(r'^$', company_leads, name='operation_company_leads'),
                       url(r'^lead/(?P<company_id>\d+)/(?P<log_type>.+)/$', download_leads, name='operation_download_leads'),
)