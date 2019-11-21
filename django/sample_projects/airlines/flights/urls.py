from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("flight/", views.flights,name='flights'),
    path("flight/<int:flight_id>/", views.flight_details,name="flight_details"),
    path("airport/", views.airports,name='airports'),
    path("airport/<int:airport_id>/", views.airport_details,name='airport_details'),
    path("flight/<int:flight_id>/book/", views.flight_details,name='book'),
    path("courier/", views.courier_claim,name='courier_claim'),
]