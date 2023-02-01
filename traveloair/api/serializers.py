import re
from rest_framework import serializers

from api.models import Flight, Passenger, Reservation


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('id', 'number', 'airline', 'departure_city',
                  'arrival_city', 'date_of_departure', 'departure_time')

    def validate_number(self, value):
        SPECIAL_CHARACTERS_NOT_ALLOWED = '!@#$%^&*'
        if any(char in SPECIAL_CHARACTERS_NOT_ALLOWED for char in value):
            raise serializers.ValidationError(
                f'Special Characters are not allowed - "{SPECIAL_CHARACTERS_NOT_ALLOWED}"')
        return value


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'flight', 'passenger')
