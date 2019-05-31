import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until DB is available"""

    def handle(self, *args, **options):
        self.stdout.write('waiting......')
        connection = None

        while not connection:
            try:
                connection = connections['default']
            except OperationalError:
                self.stdout.write('waiting for 1 second....')
                time.sleep(1)

        self.stdout.write('DB available....')
