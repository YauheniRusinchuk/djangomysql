from django.core.management.base import BaseCommand
from main.models import recreate_mock_movies


class Command(BaseCommand):
    help = 'Удаляет все фильмы и создаёт мок-данные с категориями'

    def handle(self, *args, **kwargs):
        recreate_mock_movies()
        self.stdout.write(self.style.SUCCESS(
            'Мок-данные фильмов успешно пересозданы с категориями!'))
