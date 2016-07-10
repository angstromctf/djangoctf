from django.conf.urls import include, url
from django.contrib import admin

app_name = 'learn'
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls')),
    url(r'^learn/', include('learn.urls')),
]
