from django.core.management.base import BaseCommand
from main.models import Movie


class Command(BaseCommand):
    help = 'Показывает все фильмы и их категории.'

    def handle(self, *args, **kwargs):
        for m in Movie.objects.all():
            self.stdout.write(
                f'{m.title} | category: {m.category} | category_id: {m.category_id}')
