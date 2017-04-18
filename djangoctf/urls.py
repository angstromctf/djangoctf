from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from api import views


router = DefaultRouter()
router.register('problems', views.ProblemViewSet)
router.register('teams', views.TeamViewSet)
router.register('users', views.UserViewSet)

schema_view = get_swagger_view(title='djangoctf API')

urlpatterns = [
    url('^api/$', schema_view),
    url('^api/schema', views.schema),
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += router.urls
