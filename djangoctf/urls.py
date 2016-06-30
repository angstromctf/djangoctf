from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'djangoctf.views.home', name='home'),
    # Explanation - 
    # r'^$' is the regex for the url that the view corresponds to.
    # 'djangoctf.views.home' is the view itself.  
    # name='home' is the name of the view
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ctfapp.urls')),
]
