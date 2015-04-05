from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^scoreboard$', views.scoreboard, name='scoreboard'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
]
