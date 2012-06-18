from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'phones.views.home', name='home'),
    # url(r'^phones/', include('phones.foo.urls')),

	 url(r'^logviewer/report/', 'logviewer.views.download_report'),
	 url(r'^logviewer/search/', 'logviewer.views.search'),
)
