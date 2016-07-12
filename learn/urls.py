from django.conf.urls import url

from . import views

app_name = 'learn'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^module/([0-9a-zA-Z_]+)/$', views.module, name='module')
]
