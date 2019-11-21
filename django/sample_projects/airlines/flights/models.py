from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} - {self.city}({self.code})"

class Flight(models.Model):
    #origin = models.CharField(max_length= 64)
    #destination = models.CharField(max_length=64)

    origin = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name='departures')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE,related_name='arrivals')
    duration = models.IntegerField()
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.id}-{self.origin} to {self.destination}"

class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name='passengers')

    def __str__(self):
        return f"{self.first} {self.last}"

class Courier(models.Model):
    courier_company =models.CharField(max_length=24),
    courier_no = models.CharField(max_length=24),
    courier_sent_date = models.DateField(),
    courier_received_date = models.DateField(),
    courier_from_country = models.CharField(max_length=24),
    courier_to_country = models.CharField(max_length=24),
    courier_from_place = models.CharField(max_length=24),
    courier_to_place = models.CharField(max_length=24),
    employee_id = models.CharField(max_length=24),
    designation = models.CharField(max_length=24)
