from django.db.models import Case, When
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from .models import Ride, RideEvent
from .serializers import RideCreateSerializer, RideEventSerializer, RideListSerializer


class RideFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")
    rider_email = django_filters.CharFilter(
        field_name="rider__email", lookup_expr="icontains"
    )

    class Meta:
        model = Ride
        fields = [
            "status",
            "rider_email",
        ]


class RidePagination(PageNumberPagination):
    page_size = 10


class RideViewSet(viewsets.ModelViewSet):
    queryset = (
        Ride.objects.select_related("id_rider", "id_driver")
        .prefetch_related("events")
        .all()
    )
    pagination_class = RidePagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RideFilter
    ordering_fields = ["pickup_time"]

    def get_queryset(self):
        # Get the base queryset with related objects prefetched
        queryset = (
            Ride.objects.select_related("id_rider", "id_driver")
            .prefetch_related(
                "events",
            )
            .all()
        )

        # Handle sorting by distance
        sort_by = self.request.query_params.get("sort_by", "pickup_time")

        if sort_by in ["distance", "-distance"]:
            lat = self.request.query_params.get("latitude", 0)
            lon = self.request.query_params.get("longitude", 0)
            if not lat or not lon:

                raise ValidationError(
                    {
                        "detail": "`latitude` and `longitude` must be provided for distance sorting."
                    }
                )

            try:
                user_lat = float(lat)
                user_lon = float(lon)
            except ValueError:
                raise ValidationError(
                    {"detail": "`latitude` and `longitude` must be valid numbers."}
                )

            # Calculate distances and sort
            rides_with_distances = []
            for ride in queryset:
                distance = ride.haversine_distance(
                    user_lat, user_lon, ride.pickup_latitude, ride.pickup_longitude
                )
                rides_with_distances.append((ride, distance))

            # Sort rides based on the computed distance
            reverse = True if sort_by == "distance" else False
            rides_with_distances.sort(key=lambda x: x[1], reverse=reverse)

            # Extract sorted rides
            sorted_rides = [ride.pk for ride, _ in rides_with_distances]

            preserved = Case(
                *[When(pk=pk, then=pos) for pos, pk in enumerate(sorted_rides)]
            )

            queryset = queryset.filter(pk__in=sorted_rides).order_by(preserved)

            return queryset

        return queryset.order_by(sort_by)

    def get_serializer_class(self):
        if self.action == "list":
            return RideListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return RideCreateSerializer
        return RideListSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    pagination_class = RidePagination
