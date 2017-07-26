from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('problems', views.ProblemViewSet)
router.register('teams', views.TeamViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    url('^api/schema', views.schema),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
