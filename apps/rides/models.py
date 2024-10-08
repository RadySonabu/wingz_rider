from math import atan2, cos, radians, sin, sqrt

from django.conf import settings
from django.db import models


class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("en-route", "En Route"),
            ("pickup", "Pickup"),
            ("dropoff", "Dropoff"),
        ],
    )
    id_rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rides_as_rider",
        on_delete=models.CASCADE,
    )
    id_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rides_as_driver",
        on_delete=models.CASCADE,
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id_ride} from ({self.pickup_latitude}, {self.pickup_longitude}) to ({self.dropoff_latitude}, {self.dropoff_longitude})"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    ride = models.ForeignKey(Ride, related_name="events", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id_ride_event} for Ride {self.ride.id_ride} - {self.description}"
