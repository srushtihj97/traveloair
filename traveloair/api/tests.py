import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from api.models import (
    Flight,
    Passenger,
    Reservation,
)
from api.serializers import (
    FlightSerializer,
    PassengerSerializer,
    ReservationSerializer
)
# Create your tests here.


class FlightAPIViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.flight = Flight.objects.create(
            number='A2000',
            airline='United',
            departure_city='Newark',
            arrival_city='Miami',
            date_of_departure='2021-01-22',
            departure_time='00:00:00',
        )
        self.url = f'/flights/{self.flight.id}/'

    def test_flight_object_detail(self):
        """
        Test to verify Flight object detail
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        flight_serializer_data = FlightSerializer(instance=self.flight).data
        response_data = json.loads(response.content)
        self.assertEqual(flight_serializer_data, response_data)

    def test_flight_object_update(self):
        data = {
            'number': 'A2000',
            'airline': 'United',
            'departure_city': 'New York',
            'arrival_city': 'Miami'
        }
        response = self.client.put(self.url, data)
        response_data = json.loads(response.content)
        flight = Flight.objects.get(id=self.flight.id)
        self.assertEqual(response_data.get("departure_city"),
                         flight.departure_city)

    def test_flight_object_partial_update(self):
        data = {'airline': 'Spirit'}
        response = self.client.patch(self.url, data)
        response_data = json.loads(response.content)
        flight = Flight.objects.get(id=self.flight.id)
        self.assertEqual(response_data.get("airline"), flight.airline)

    def test_flight_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


class PassengerAPIViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.passenger = Passenger.objects.create(
            first_name="John",
            last_name="Fow",
            email="john.fow@google.com",
            phone_number="+19021200122",
        )
        self.url = f'/passengers/{self.passenger.id}/'

    def test_passenger_object_detail(self):
        """
        Test to verify Passenger object detail
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        passenger_serializer_data = PassengerSerializer(
            instance=self.passenger).data
        response_data = json.loads(response.content)
        self.assertEqual(passenger_serializer_data, response_data)

    def test_passenger_object_update(self):
        data = {
            'first_name': 'Bobby',
            'last_name': 'David',
            'email': 'bobby.david@google.com',
            'phone_number': '+198271289209'
        }
        response = self.client.put(self.url, data)
        response_data = json.loads(response.content)
        passenger = Passenger.objects.get(id=self.passenger.id)
        self.assertEqual(response_data.get("first_name"),
                         passenger.first_name)

    def test_passenger_object_partial_update(self):
        data = {'first_name': 'Matt'}
        response = self.client.patch(self.url, data)
        response_data = json.loads(response.content)
        passenger = Passenger.objects.get(id=self.passenger.id)
        self.assertEqual(response_data.get("first_name"), passenger.first_name)

    def test_passenger_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


class ReservationAPIViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.flight = Flight.objects.create(
            number='A1000',
            airline='United',
            departure_city='Newark',
            arrival_city='Miami',
            date_of_departure='2021-01-22',
            departure_time='00:00:00',
        )
        self.passenger = Passenger.objects.create(
            first_name="John",
            last_name="Fow",
            email="john.fow@google.com",
            phone_number="+19021200122",
        )
        self.reservation = Reservation.objects.create(
            flight=self.flight,
            passenger=self.passenger,
        )
        self.url = f'/reservations/{self.reservation.id}/'

    def test_reservation_object_detail(self):
        """
        Test to verify Reservation object detail
        """
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        reservation_serializer_data = ReservationSerializer(
            instance=self.reservation).data
        response_data = json.loads(response.content)
        self.assertEqual(reservation_serializer_data, response_data)

    def test_reservation_object_update(self):
        self.flight_2 = Flight.objects.create(
            number='A3000',
            airline='United',
            departure_city='Newark',
            arrival_city='Miami',
            date_of_departure='2021-01-22',
            departure_time='00:00:00',
        )
        data = {
            'flight': self.flight_2.id,
            'passenger': self.passenger.id,
        }
        response = self.client.put(self.url, data)
        response_data = json.loads(response.content)
        reservation = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(response_data.get("flight"),
                         reservation.flight.id)
        self.flight_2.delete()

    def test_reservation_object_partial_update(self):
        self.flight_3 = Flight.objects.create(
            number='A4000',
            airline='United',
            departure_city='Newark',
            arrival_city='Miami',
            date_of_departure='2021-01-22',
            departure_time='00:00:00',
        )
        data = {'flight': self.flight_3.id}
        response = self.client.patch(self.url, data)
        response_data = json.loads(response.content)
        reservation = Reservation.objects.get(id=self.reservation.id)
        self.assertEqual(response_data.get("flight"), reservation.flight.id)

    def test_reservation_object_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


class FindFlightsAPIViewTestCase(APITestCase):
    url = '/findFlights'

    def setUp(self):
        flights = [{
            'number': 'A2001',
            'airline': 'United',
            'departure_city': 'New York',
            'arrival_city': 'Chicago',
            'date_of_departure': '2021-08-12',
            'departure_time': '00:00:00'
        }, {
            'number': 'A2002',
            'airline': 'United',
            'departure_city': 'New York',
            'arrival_city': 'San Jose',
            'date_of_departure': '2021-08-14',
            'departure_time': '00:00:00'
        }, {
            'number': 'A2003',
            'airline': 'United',
            'departure_city': 'Las Vegas',
            'arrival_city': 'Chicago',
            'date_of_departure': '2021-08-21',
            'departure_time': '00:00:00'
        }, {
            'number': 'A2004',
            'airline': 'United',
            'departure_city': 'New York',
            'arrival_city': 'Miami',
            'date_of_departure': '2021-09-12',
            'departure_time': '00:00:00'
        }]
        for flight in flights:
            Flight.objects.create(**flight)

    def test_find_flights_departing_new_york(self):
        params = {
            'departure_city': 'New York'
        }
        response = self.client.get(self.url, params)
        response_data = json.loads(response.content)
        self.assertEqual(3, len(response_data))

    def test_find_flights_departing_new_york_on_or_after_august_14_2021(self):
        params = {
            'departure_city': 'New York',
            'date_of_departure__gte': '2021-08-14'
        }
        response = self.client.get(self.url, params)
        response_data = json.loads(response.content)
        self.assertEqual(2, len(response_data))

    def test_find_flights_new_york_to_miami(self):
        params = {
            'departure_city': 'New York',
            'arrival_city': 'Miami'
        }
        response = self.client.get(self.url, params)
        response_data = json.loads(response.content)
        self.assertEqual(1, len(response_data))

    def test_find_flights_arriving_in_chicago(self):
        params = {
            'arrival_city': 'Chicago'
        }
        response = self.client.get(self.url, params)
        response_data = json.loads(response.content)
        self.assertEqual(2, len(response_data))


class SaveReservationAPIViewTestCase(APITestCase):
    url = '/saveReservation'

    def setUp(self):
        self.flight = Flight.objects.create(
            number='A1000',
            airline='United',
            departure_city='Newark',
            arrival_city='Miami',
            date_of_departure='2021-01-22',
            departure_time='00:00:00',
        )
        self.passenger = Passenger.objects.create(
            first_name="John",
            last_name="Fow",
            email="john.fow@google.com",
            phone_number="+19021200122",
        )

    def test_save_reservation(self):
        data = {'flight_id': self.flight.id,
                'passenger_id': self.passenger.id}
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
