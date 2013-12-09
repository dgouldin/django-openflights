# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import csv, datetime, sys

from django.core.management.base import BaseCommand

from ... import loaders


class Command(BaseCommand):
    args = '<loader filename ...>'
    help = """Loads the specified OpenFlights object type using the data file
              at `filename`"""

    def handle(self, *args, **options):
        start = datetime.datetime.now()
        loader, filename = args
        load = getattr(loaders, 'load_{0}'.format(loader))
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                load(row)
                if i % 100 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
        end = datetime.datetime.now()
        sys.stdout.write('\nLoading complete. ({0} in {1}s)\n'.format(
            (i + 1), (end - start).seconds))
