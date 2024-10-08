# Generated by Django 5.0.7 on 2024-08-02 18:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ride",
            fields=[
                ("id_ride", models.AutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("en-route", "En Route"),
                            ("pickup", "Pickup"),
                            ("dropoff", "Dropoff"),
                        ],
                        max_length=50,
                    ),
                ),
                ("pickup_latitude", models.FloatField()),
                ("pickup_longitude", models.FloatField()),
                ("dropoff_latitude", models.FloatField()),
                ("dropoff_longitude", models.FloatField()),
                ("pickup_time", models.DateTimeField()),
                (
                    "driver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rides_as_driver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rides_as_rider",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RideEvent",
            fields=[
                ("id_ride_event", models.AutoField(primary_key=True, serialize=False)),
                ("description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "ride",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="rides.ride",
                    ),
                ),
            ],
        ),
    ]
