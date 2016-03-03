from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

from django.contrib.auth import views as auth_views

"""
URL patterns used by django to load views.
"""
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^shelld/$', views.shelld, name='shelld'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^about/', views.about, name='about'),
    url(r'^rules/', views.rules, name='rules'),
    url(r'^learn/', views.learn, name='learn'),
    url(r'^chat/', views.chat, name='chat'),
    url(r'^sponsors/', views.sponsors, name='sponsors'),

    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^score/', views.score, name='score'),
    url(r'^profile/(?P<team>[a-zA-Z0-9]*)$', views.profile),

    url(r'^problems/$', views.problems, name='problems'),
    url(r'^problems/submit_problem/$', views.submit_problem, name='submit_problem'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/change_password/$', views.change_password, name='change_password'),
    url(r'^account/create_team/$', views.create_team, name='create_team'),
    url(r'^account/join_team/$', views.join_team, name='join_team'),
    url(r'^account/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^account/logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^account/signup/$', views.signup, name='signup'),

    url(r'^resetpassword/$', auth_views.password_reset,
        {'post_reset_redirect' : 'passwordsent/',
         'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^resetpassword/passwordsent/', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',  auth_views.password_reset_confirm, {'post_reset_redirect' : '/reset/done/'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^activate/(?P<key>.+)/$', views.activation, name='activation'),
    url(r'^new-activation-link/(?P<user_id>\d+)/$', views.new_activation_link, name='new_link'),
]
