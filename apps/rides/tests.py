from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ride, RideEvent

User = get_user_model()


class RideListViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            role="rider",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890",
        )
        self.user2 = User.objects.create(
            role="driver",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone_number="0987654321",
        )

        self.ride1 = Ride.objects.create(
            status="completed",
            id_rider=self.user1,
            id_driver=self.user2,
            pickup_latitude=17.0,
            pickup_longitude=205.0,
            dropoff_latitude=17.0,
            dropoff_longitude=3.0,
            pickup_time=timezone.now() - timedelta(days=1),
        )
        self.ride2 = Ride.objects.create(
            status="completed",
            id_rider=self.user1,
            id_driver=self.user2,
            pickup_latitude=230.0,
            pickup_longitude=200.0,
            dropoff_latitude=170.0,
            dropoff_longitude=270.0,
            pickup_time=timezone.now() - timedelta(hours=23),
        )
        self.ride3 = Ride.objects.create(
            status="completed",
            id_rider=self.user1,
            id_driver=self.user2,
            pickup_latitude=15.0,
            pickup_longitude=200.0,
            dropoff_latitude=17.0,
            dropoff_longitude=2.0,
            pickup_time=timezone.now() - timedelta(hours=20),
        )

        self.ride_event1 = RideEvent.objects.create(
            ride=self.ride1,
            description="Pickup completed",
            created_at=timezone.now() - timedelta(hours=23),
        )
        self.ride_event2 = RideEvent.objects.create(
            ride=self.ride2,
            description="Dropoff completed",
            created_at=timezone.now() - timedelta(hours=22),
        )

    def test_sorting_by_default(self):
        """Tests the default sorting of Ride List API."""

        url = reverse("rides-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["id_ride"], self.ride1.id_ride
        )  # 1
        self.assertEqual(
            response.data["results"][1]["id_ride"], self.ride2.id_ride
        )  # 2
        self.assertEqual(
            response.data["results"][2]["id_ride"], self.ride3.id_ride
        )  # 3

    def test_distance_sorting_across_pages(self):
        """Tests that the sorting is applied across all pages."""

        url = (
            reverse("rides-list")
            + "?sort_by=distance&latitude=15.0&longitude=200.0&page=1&page_size=2"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["id_ride"], self.ride3.id_ride
        )  # 3
        self.assertEqual(
            response.data["results"][1]["id_ride"], self.ride1.id_ride
        )  # 1

        url = (
            reverse("rides-list")
            + "?sort_by=distance&latitude=15.0&longitude=200.0&page=2&page_size=2"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["id_ride"], self.ride2.id_ride
        )  # 3
