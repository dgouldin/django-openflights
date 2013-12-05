from django.db import models

class Airport(models.Model):

    DST_EUROPE = 'E'
    DST_US_CANADA = 'A'
    DST_SOUTH_AMERICA = 'S'
    DST_AUSTRALIA = 'O'
    DST_NEW_ZEALAND = 'Z'
    DST_NONE = 'N'
    DST_UNKNOWN = 'U'

    DST_CHOICES = (
        (DST_EUROPE, 'Europe'),
        (DST_US_CANADA, 'US/Canada'),
        (DST_SOUTH_AMERICA, 'South America'),
        (DST_AUSTRALIA, 'Australia'),
        (DST_NEW_ZEALAND, 'New Zealand'),
        (DST_NONE, 'None'),
        (DST_UNKNOWN, 'Unkonwn'),
    )

    airport_id = models.PositiveSmallIntegerField(db_index=True)
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    iata_faa = models.CharField(max_length=3, blank=True)
    icao = models.CharField(max_length=4, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.IntegerField()
    timezone = models.DecimalField(max_digits=4, decimal_places=2)
    dst = models.CharField(max_length=1, choices=DST_CHOICES)

class Airline(models.Model):
    pass

class Route(models.Model):
    pass

class Schedule(models.Model):
    pass