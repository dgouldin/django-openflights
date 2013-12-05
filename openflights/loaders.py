from __future__ import absolute_import

from .models import Airport, Airline, Route


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

    return airline

def load_route(row):
    row_cleaned = ['' if i == '\N' else i for i in row]
    (
        _, airline_id,
        _, source_airport_id,
        _, dest_airport_id,
        codeshare,
        stops,
        equipment,
    ) = row_cleaned

    if not all([airline_id, source_airport_id, dest_airport_id]):
        return

    airline = Airline.objects.get(airline_id=airline_id)
    source_airport = Airport.objects.get(airport_id=source_airport_id)
    dest_airport = Airport.objects.get(airport_id=dest_airport_id)
    codeshare = codeshare == 'Y'

    route, _ = Route.objects.update_or_create(airline=airline,
                                              source_airport=source_airport,
                                              destination_airport=dest_airport,
                                              defaults={
                                                  'codeshare': codeshare,
                                                  'stops': stops,
                                                  'equipment': equipment,
                                              })

    return route
