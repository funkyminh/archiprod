# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from haystack.query import SearchQuerySet

from archives.views import CustomSearchView
import autocomplete_light

from archives.forms import FilterSearchForm

# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

admin.autodiscover()

sqs = SearchQuerySet().facet('set').facet('event_type').facet('media_type').facet('is_sound').facet('year')

urlpatterns = patterns('',
    url(r'^$', 'archives.views.home', name='home'),
    url(r'^upload$', 'archives.views.upload', name='upload'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^(?P<slug>[-\w]+)$', 'archives.views.detail', name='detail'),
    url(r'^search/$', CustomSearchView(form_class=FilterSearchForm, searchqueryset=sqs), name='haystack_search'),
    url(r'^embed/media/(?P<slug>[-\w]+)$', 'archives.views.embed_media', name='embed_media'),
    url(r'^download/(?P<text>.*)$', 'archives.views.download', name='download'),
    url(r'^embed/playlist/$', 'archives.views.playlist', name='playlist'),
    (r'^admin/rq/', include('django_rq_dashboard.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^progressbarupload/', include('progressbarupload.urls')),
    (r'^django-rq/', include('django_rq.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT,  'show_indexes': True}),
                            url(r'^stream/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STREAM_ROOT,  'show_indexes': True}))
    urlpatterns += staticfiles_urlpatterns()

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
