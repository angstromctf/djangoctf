from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'djangoctf.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ctfapp.urls')),
]
