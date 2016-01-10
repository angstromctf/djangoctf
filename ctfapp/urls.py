from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^problems/submit_problem/$', views.submit_problem, name='submit_problem'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/change_password/$', views.change_password, name='change_password'),
    url(r'^account/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^account/logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^account/signup/$', views.signup, name='signup'),
    url(r'^profile/(?P<user>[a-zA-Z0-9]*)$', views.profile),
    url(r'^about/', views.about, name='about'),
    url(r'^chat/', views.chat, name='chat'),
    url(r'^score/', views.score, name='score')
]
