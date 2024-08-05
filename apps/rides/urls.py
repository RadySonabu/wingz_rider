from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideEventViewSet

rides_router = DefaultRouter()
rides_router.register(r"rides", RideViewSet, "rides")
rides_router.register(r"rides-events", RideEventViewSet, "rides-events")

urlpatterns = [
    path("api/rides/", include(rides_router.urls)),
]
