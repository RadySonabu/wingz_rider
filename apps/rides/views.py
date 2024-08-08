from django.db.models import ExpressionWrapper, F, FloatField, Prefetch
from django.db.models.functions import Cos, Power, Radians, Sin, Sqrt
from django.utils import timezone
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

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


class RidePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class RideViewSet(viewsets.ModelViewSet):
    pagination_class = RidePagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RideFilter
    ordering_fields = ["pickup_time", "distance"]

    def get_queryset(self):

        today = timezone.now()
        last_24_hours = today - timezone.timedelta(hours=24)

        # ride_events_24_hours filters RideEvent object/s created outside the 24 hour period.
        ride_events_24_hours = Prefetch(
            "events",
            queryset=RideEvent.objects.select_related(
                "ride",
            ).filter(created_at__gte=last_24_hours),
        )

        queryset = Ride.objects.select_related(
            "id_rider", "id_driver"
        ).prefetch_related(ride_events_24_hours)

        # Handle sorting by distance
        sort_by = self.request.query_params.get("sort_by", "pickup_time")

        if sort_by in ["distance", "-distance"]:
            try:
                lat = self.request.query_params.get("latitude", 0)
                lon = self.request.query_params.get("longitude", 0)

                if not lat or not lon:
                    raise ValidationError(
                        {
                            "detail": "`latitude` and `longitude` must be provided for distance sorting."
                        }
                    )
                user_latitude_radians = Radians(float(lat))
                user_longitude_radians = Radians(float(lon))
            except ValueError:
                raise ValidationError(
                    {"detail": "`latitude` and `longitude` must be valid numbers."}
                )

            distance_expression = ExpressionWrapper(
                6371
                * 2
                * Radians(
                    Sqrt(
                        Power(
                            Sin(
                                (Radians(F("pickup_latitude")) - user_latitude_radians)
                                / 2
                            ),
                            2,
                        )
                        + Cos(user_latitude_radians)
                        * Cos(Radians(F("pickup_latitude")))
                        * Power(
                            Sin(
                                (
                                    Radians(F("pickup_longitude"))
                                    - user_longitude_radians
                                )
                                / 2
                            ),
                            2,
                        )
                    )
                ),
                output_field=FloatField(),
            )

            limit = int(self.request.query_params.get("limit", 100))
            offset = int(self.request.query_params.get("offset", 0))
            queryset = queryset.annotate(distance=distance_expression).order_by(
                sort_by
            )[
                max(0, offset - 1) : limit
            ]  # [1: 2]

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
