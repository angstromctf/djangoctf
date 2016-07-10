from django.conf.urls import url

from . import views


"""
URL patterns used by django to load views.
"""


urlpatterns = [
    url(r'^$', views.index, name='home'),
]
