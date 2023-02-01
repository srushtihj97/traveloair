from django.db import models
from datetime import date, time


# Create your models here.
class Flight(models.Model):
    number = models.CharField(max_length=100,
                              unique=True,
                              null=False)
    airline = models.CharField(max_length=100)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    date_of_departure = models.DateField(default=date)
    departure_time = models.TimeField(default=time)

    class Meta:
        db_table = 'pluto_flights'
        verbose_name = 'Flight'

    def __str__(self):
        return f'Flight (flight_number={self.number}, airline={self.airline})'


class Passenger(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    phone_number = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'pluto_passengers'
        verbose_name = 'Passenger'

    def __str__(self):
        return f'Passenger (first_name={self.first_name}, last_name={self.last_name})'


class Reservation(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    passenger = models.OneToOneField(Passenger,
                                     on_delete=models.CASCADE)

    class Meta:
        db_table = 'pluto_reservations'
        verbose_name = 'Reservation'

    def __str__(self):
        return f'Reservation (flight={self.flight}, passenger={self.passenger})'
