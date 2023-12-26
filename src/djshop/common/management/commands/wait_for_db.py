"""
Django command to wait for the database to be available.
"""

import time
from typing import Any

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """
    Django's management command that waits for the database
    to be available before proceeding.
    """

    def handle(self, *args: Any, **options: Any) -> None:

        """
        Command's entry point that continuously checks for database availability.

        :param args: Additional command-line arguments
        :param options: Additional options
        :return: None
        """

        self.stdout.write('Waiting for database...')
        db_available = False

        while db_available is False:
            try:
                # Check if the default database is available.
                self.check(databases=['default'])
                db_available = True
            except (OperationalError, Psycopg2Error):
                # If the database is unavailable, wait for 1 second before
                # reattempting.
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
