from __future__ import absolute_import

import math

from django.db import models

from .managers import BaseManager

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

    airport_id = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    iata_faa = models.CharField(max_length=3, blank=True)
    icao = models.CharField(max_length=4, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.IntegerField()
    timezone = models.DecimalField(max_digits=5, decimal_places=2)
    dst = models.CharField(max_length=1, choices=DST_CHOICES)

    objects = BaseManager()

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.iata_faa)

    def distance_to(self, airport):
        EARTH_RADIUS = 3958.761 # in miles
        lat1 = self.latitude
        lon1 = self.longitude
        lat2 = airport.latitude
        lon2 = airport.longitude

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
                math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                math.sin(d_lon / 2) * math.sin(d_lon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return int(EARTH_RADIUS * c)

class Airline(models.Model):
    airline_id = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=1000)
    alias = models.CharField(max_length=1000)
    iata = models.CharField(max_length=2)
    icao = models.CharField(max_length=3)
    callsign = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    active = models.BooleanField()

    objects = BaseManager()

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.callsign)


class Route(models.Model):
    airline = models.ForeignKey(Airline, related_name='routes')
    source_airport = models.ForeignKey(Airport, related_name='source_routes')
    destination_airport = models.ForeignKey(Airport,
                                            related_name='destination_routes')
    codeshare = models.BooleanField()
    stops = models.IntegerField()
    equipment = models.CharField(max_length=1000)
    distance = models.IntegerField()

    objects = BaseManager()

    class Meta:
        unique_together = (
            ('airline', 'source_airport', 'destination_airport'),
        )

    def __unicode__(self):
        return '{0}: {1} -> {2}'.format(self.airline.callsign,
                                        self.source_airport.iata_faa,
                                        self.destination_airport.iata_faa)

    def refresh_distance(self):
        self.distance = self.source_airport.distance_to(self.destination_airport)

    def save(self, force_refresh_distance=False, *args, **kwargs):
        if self.distance is None or force_refresh_distance:
            self.refresh_distance()
        super(Route, self).save(*args, **kwargs)
