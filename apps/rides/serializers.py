from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Ride, RideEvent


User = get_user_model()


class RideEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideEvent
        fields = "__all__"


class RideListSerializer(serializers.ModelSerializer):

    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    todays_ride_events = RideEventSerializer(
        many=True, read_only=True, source="limited_ride_events_24_hours"
    )

    class Meta:
        model = Ride
        fields = [
            "id_ride",
            "status",
            "id_rider",
            "id_driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "todays_ride_events",
        ]


class RideCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = "__all__"
