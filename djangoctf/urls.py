from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from api import views


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, CoreJSONRenderer])
def schema_view(request):
    generator = SchemaGenerator(title='Pastebin API')
    return Response(generator.get_schema(request=request))


router = DefaultRouter()
router.register('problems', views.ProblemViewSet)
router.register('teams', views.TeamViewSet)

urlpatterns = [
    url('^$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]