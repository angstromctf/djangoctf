from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('problems', views.ProblemViewSet)
router.register('teams', views.TeamViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('schema/', views.schema),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
