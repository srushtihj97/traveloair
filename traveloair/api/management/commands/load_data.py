import json
import random
from django.core.management.base import BaseCommand
from api.models import Passenger, Flight, Reservation


class Command(BaseCommand):
    help = "Load Passenger, Flight and Reservation data"

    def load_file(self, file_name):
        with open(file_name) as f:
            data = json.loads(f.read())
        return data

    def handle(self, *args, **options):
        if Passenger.objects.count() or Flight.objects.count():
            return
        passengers = self.load_file('data/passengers.json')
        passenger_ids = []
        for passenger in passengers:
            obj = Passenger.objects.create(**passenger)
            passenger_ids.append(obj.id)

        flights = self.load_file('data/flights.json')
        flight_ids = []
        for flight in flights:
            obj = Flight.objects.create(**flight)
            flight_ids.append(obj.id)

        for passenger_id in passenger_ids:
            Reservation.objects.create(flight_id=random.choice(flight_ids),
                                       passenger_id=passenger_id)
