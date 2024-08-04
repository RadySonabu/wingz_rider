from django.contrib import admin
from django.urls import path, include

from rest_framework.views import APIView
from rest_framework.response import Response
from debug_toolbar.toolbar import debug_toolbar_urls


class APIRoot(APIView):

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "users": request.build_absolute_uri("/api/users/"),
                "rides": request.build_absolute_uri("/api/rides/"),
            }
        )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", APIRoot.as_view(), name="api-root"),
    path("", include("apps.rides.urls")),
    path("", include("apps.users.urls")),
    path("api-auth/", include("rest_framework.urls")),
] + debug_toolbar_urls()
