from __future__ import absolute_import

from .models import Airport, Airline


def load_airport(row):
    field_names = (
        'airport_id',
        'name',
        'city',
        'country',
        'iata_faa',
        'icao',
        'latitude',
        'longitude',
        'altitude',
        'timezone',
        'dst',
    )
    defaults = dict(zip(field_names, row))
    airport_id = defaults.pop('airport_id')
    airport, _ = Airport.objects.update_or_create(airport_id=airport_id,
                                                  defaults=defaults)
    return airport

def load_airline(row):
    field_names = (
        'airline_id',
        'name',
        'alias',
        'iata',
        'icao',
        'callsign',
        'country',
        'active',
    )
    defaults = dict(zip(field_names, row))
    airline_id = defaults.pop('airline_id')
    defaults['active'] = defaults['active'] == 'Y'
    airline, _ = Airline.objects.update_or_create(airline_id=airline_id,
                                                 defaults=defaults)
