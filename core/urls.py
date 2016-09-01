from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^shelld/$', views.shelld, name='shelld'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^about/', views.about, name='about'),
    url(r'^chat/', views.chat, name='chat'),
    url(r'^sponsors/', views.sponsors, name='sponsors'),
    url(r'^unsubscribe_success/', views.unsubscribe, name='unsubscribe'),
    url(r'^score/', views.score, name='score'),

    url(r'^scoreboard/$', views.scoreboard, name='scoreboard'),
    url(r'^scoreboard/feed/$', views.jsonfeed, name='jsonfeed'),

    url(r'^team/profile/(\d+)$', views.profile, name='profile'),
    url(r'^team/create/$', views.create_team, name='create_team'),
    url(r'^team/join/$', views.join_team, name='join_team'),
    url(r'^team/submit_addr/$', views.submit_addr, name='submit_addr'),
    url(r'^team/leave_team/$', views.leave_team, name='leave_team'),

    url(r'^problems/$', views.problems, name='problems'),
    url(r'^problems/submit/$', views.submit_problem, name='submit_problem'),

    url(r'^account/$', views.account, name='account'),
    url(r'^account/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^account/logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^account/signup/$', views.signup, name='signup'),
    url(r'^account/activate/(?P<key>.+)/$', views.activation, name='activation'),
    url(r'^account/activate/new/(?P<user_id>\d+)/$', views.new_activation_link, name='new_link'),

    url(r'^account/password/change/$', views.change_password, name='change_password'),
    url(r'^account/password/reset/$', auth_views.password_reset,
        {'post_reset_redirect' : 'sent/',
         'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^account/password/reset/sent', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^account/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',  auth_views.password_reset_confirm,
        {'post_reset_redirect': '/reset/done/'}, name='password_reset_confirm'),
    url(r'^account/password/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
