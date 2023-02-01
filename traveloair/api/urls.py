from django.urls import include, path

from rest_framework import routers

from api.views import (
    FlightViewSet,
    FlightSearchViewSet,
    PassengerViewSet,
    ReservationViewSet,
    SaveReservationView,
)

router = routers.DefaultRouter()
router.register(r'flights', FlightViewSet)
# router.register(r'findFlights', FlightSearchViewSet)
router.register(r'passengers', PassengerViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('saveReservation', SaveReservationView.as_view(), name='save-reservation'),
    path('findFlights', FlightSearchViewSet.as_view(), name='find-reservation'),
]
