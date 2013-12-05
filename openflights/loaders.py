from __future__ import absolute_import

from .models import Airport


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
    try:
        airport, _ = Airport.objects.update_or_create(airport_id=airport_id,
                                                      defaults=defaults)
    except Exception as e:
        import ipdb; ipdb.set_trace()
    return airport
