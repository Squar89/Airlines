from django.db import models
from django.core.validators import MinValueValidator


class Airplane(models.Model):
    registration = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.registration


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Passenger(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Crew(models.Model):
    c_first_name = models.CharField(max_length=30)
    c_last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.c_first_name + " " + self.c_last_name


class Flight(models.Model):
    airplane = models.ForeignKey(Airplane, on_delete=models.PROTECT)
    city_from = models.ForeignKey(City, on_delete=models.PROTECT, related_name='flights_from')
    city_to = models.ForeignKey(City, on_delete=models.PROTECT, related_name='flights_to')
    date_dep = models.DateTimeField('departure_date')
    date_arr = models.DateTimeField('arrival_date')
    passengers = models.ManyToManyField(Passenger, default=[])
    crew = models.ForeignKey(Crew, on_delete=models.PROTECT, blank=True, null=True, default=None)

    def __str__(self):
        return "Flight from %s to %s" % (self.city_from, self.city_to)
