import django_filters
from django.shortcuts import render
from django.db.utils import IntegrityError
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import filters

from api.serializers import (
    FlightSerializer,
    PassengerSerializer,
    ReservationSerializer,
)

from api.models import (
    Flight,
    Passenger,
    Reservation,
)


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class SaveReservationView(generics.CreateAPIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        flight_id = request.data.get('flight_id')
        passenger_id = request.data.get('passenger_id')
        if not flight_id:
            return Response(
                data='Flight ID should be specified',
                status=status.HTTP_400_BAD_REQUEST
            )
        if not passenger_id:
            return Response(
                data='Passenger ID should be specified',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            reservation = Reservation.objects.create(
                flight_id=flight_id,
                passenger_id=passenger_id)
        except IntegrityError as e:
            msg = {
                'error': f"Reservation for Passenger ({passenger_id}) already exists."}
            return Response(data=msg,
                            status=status.HTTP_400_BAD_REQUEST)
        data = {
            'message': f'Reservation ({reservation.id}) was successfully made for Passenger ({passenger_id}).'
        }
        return Response(data=data,
                        status=status.HTTP_200_OK)


class FlightFilterSet(django_filters.FilterSet):
    class Meta:
        model = Flight
        fields = ['departure_city', 'arrival_city', 'date_of_departure']
        fields = {
            'departure_city': ['exact'],
            'arrival_city': ['exact'],
            'date_of_departure': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }


class FlightSearchViewSet(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    filterset_class = FlightFilterSet
    ordering_fields = ('date_of_departure', 'departure_time')
