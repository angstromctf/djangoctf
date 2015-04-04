from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^login/$', views.login_view, name='login'),
]
