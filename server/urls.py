from django.contrib import admin
from django.urls import path, include

# swagger docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Smart Traffic Lights monitoring and controlling with IoT and cloud computing",
      default_version='v1',
      description="""
      ### General Instructions

      1. This is the server for minor project. 
      1. Hosted Node-Red simulator can be found at http://54.194.87.141:1880/
      1. Token authentication is used.
      """,
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',schema_view.with_ui('swagger',cache_timeout=0), name = 'schema-swagger-ui'),
    path('user/', include('users.urls')),
    path('maps/', include('maps.urls')),
]
