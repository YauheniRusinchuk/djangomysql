import time
import MySQLdb
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_settings = settings.DATABASES['default']
        attempts = 0
        max_attempts = 30  # Maximum number of attempts

        while attempts < max_attempts:
            try:
                conn = MySQLdb.connect(
                    host=db_settings['HOST'],
                    user=db_settings['USER'],
                    password=db_settings['PASSWORD'],
                    database=db_settings['NAME'],
                    port=int(db_settings['PORT'])
                )
                conn.close()
                self.stdout.write(self.style.SUCCESS('Database available!'))
                return
            except MySQLdb.OperationalError as e:
                attempts += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Database unavailable, attempt {attempts}/{max_attempts}. '
                        f'Error: {str(e)}. Waiting 1 second...'
                    )
                )
                time.sleep(1)

        self.stdout.write(
            self.style.WARNING(
                f'Could not connect to database after {max_attempts} attempts. '
                'Continuing without database connection...'
            )
        )
        return
