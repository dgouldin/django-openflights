# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .models import Airport, Airline, Route

def clean_row(row):
    return ['' if i == '\N' else i.replace('\\\\', '\\') for i in row]

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
    defaults = dict(zip(field_names, clean_row(row)))
    airport_id = int(defaults.pop('airport_id'))
    if airport_id <= 0:
        return

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
    defaults = dict(zip(field_names, clean_row(row)))
    airline_id = int(defaults.pop('airline_id'))
    if airline_id <= 0:
        return

    defaults['active'] = defaults['active'] == 'Y'
    try:
        airline, _ = Airline.objects.update_or_create(airline_id=airline_id,
                                                     defaults=defaults)
    except Exception as e:
        import ipdb; ipdb.set_trace();

    return airline

def load_route(row):
    (
        _, airline_id,
        _, source_airport_id,
        _, dest_airport_id,
        codeshare,
        stops,
        equipment,
    ) = clean_row(row)

    if not all([airline_id, source_airport_id, dest_airport_id]):
        return

    airline = Airline.objects.get(airline_id=airline_id)
    source_airport = Airport.objects.get(airport_id=source_airport_id)
    dest_airport = Airport.objects.get(airport_id=dest_airport_id)
    codeshare = codeshare == 'Y'
    distance = source_airport.distance_to(dest_airport)

    route, _ = Route.objects.update_or_create(airline=airline,
                                              source_airport=source_airport,
                                              destination_airport=dest_airport,
                                              defaults={
                                                  'codeshare': codeshare,
                                                  'stops': stops,
                                                  'equipment': equipment,
                                                  'distance': distance,
                                              })

    return route
