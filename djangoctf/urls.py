from django.conf.urls import include, url
from django.contrib import admin

from api import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter(schema_title='djangoctf API')
router.register(r'problems', views.ProblemViewSet)
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]