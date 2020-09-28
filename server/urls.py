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
      1. Hosted **Node-Red simulator** can be found at http://<ip-of-this-server>:1880/
      1. Token authentication is used.
      1. Test user: (username: **a108**, password: **minor123**)
      1. Sample auth token (token of a108): **"Token dbef64a307efc2df5a8cab4827a8a65833f1b5e6**"
      1. After login send the token obtained for example see above. Else you will face 401 Unauthorised
      1. The smart traffic lights algorithm is still in the works.
      1. For django admin visit /admin (username: **admin**, password: **admin**)
      1. **This interactive API can be used as an alternative to postman**.
      1. The **green authorization button** on the right side can be used to simulate login by pasting the token in the provided field. 
      1. for making a API call append the relative URL to IP of this server.
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
