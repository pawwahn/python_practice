from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Airport, Passenger, Courier
from django.urls import reverse

# Create your views here.

# def index(request):
#     return HttpResponse("Flights..!")

def index(request):
    context = {
        "flights" : Flight.objects.all(),
        "airports": Airport.objects.all(),
        "airport_codes": Airport.objects.all()
    }
    return render(request, 'flights/index.html',context)

def flight_details(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoseNotExist:
        raise Http404("Flight Does not Exist")
    context = {
        "flight" : flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight_details.html", context)

def flights(request):
    try:
        flights = Flight.objects.all()
    except Flight.DoesNotExists:
        raise Http404("No Flights defined")
    context = {
        "flights": flights,

    }
    return render(request, "flights/flights.html", context)

def airport_details(request, airport_id):
    try:
        airport = Airport.objects.get(pk=airport_id)
    except Airport.DoseNotExist:
        raise Http404("Airport Does not Exist")
    context = {
        "airport": airport
    }
    return render(request, "airports/airport_details.html", context)

def airports(request):
    try:
        airports = Airport.objects.all()
    except Airport.DoesNotExists:
        raise Http404("No Airports defined")
    context = {
        "airports": airports
    }
    return render(request, "airports/airports.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html",{"message": "No Selection"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Flight."})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {'message': "No Passengers."})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

def courier_claim(request):
    try:
        courier = Courier.objects.all()
    except Courier.DoesNotExists:
        raise Http404("No Courier defined")
    context = {
        "courier": courier
    }
    return render(request, "courier/courier.html", context)

