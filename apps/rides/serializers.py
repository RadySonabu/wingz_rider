from rest_framework import serializers

from apps.users.serializers import UserSerializer, UserSerializerReadOnly
from .models import Ride, RideEvent
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..users.models import CustomUser

User = get_user_model()


class RideEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideEvent
        fields = ["id_ride_event", "description", "created_at"]


class RideSerializer(serializers.ModelSerializer):

    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    todays_ride_events = RideEventSerializer(many=True, read_only=True, source="events")

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
