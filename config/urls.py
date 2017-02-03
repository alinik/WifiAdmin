# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from wifinder.pois.views import data_js, data_json, get_version

urlpatterns = [
                  url(r'^jet/', include('jet.urls', 'jet')),
                  url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS

                  url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
                  url(r'^pois/', include('wifinder.pois.urls'), name='data'),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
                  url(r'^js/data.js$', data_js, name='data.js'),
                  url(r'^js/data.json$', data_json, name='data.json'),
                  url(r'^version.json$', get_version, name='data.json'),

                  # Django Admin, use {% url 'admin:index' %}
                  url(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  url(r'^users/', include('wifinder.users.urls', namespace='users')),
                  url(r'^accounts/', include('allauth.urls')),

                  # Your stuff: custom urls includes go here

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if 'django_uwsgi' in settings.INSTALLED_APPS:
    urlpatterns += [url(r'^admin/uwsgi/', include('django_uwsgi.urls')), ]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
