from __future__ import absolute_import

import csv, sys

from django.core.management.base import BaseCommand

from ... import loaders


class Command(BaseCommand):
    args = '<loader filename ...>'
    help = """Loads the specified OpenFlights object type using the data file
              at `filename`"""

    def handle(self, *args, **options):
        loader, filename = args
        load = getattr(loaders, 'load_{0}'.format(loader))
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                load(row)
                sys.stdout.write('.')
                sys.stdout.flush()
