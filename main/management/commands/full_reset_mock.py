from django.core.management.base import BaseCommand
from main.models import Movie, Rating, Comment
from django.db import transaction
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Полностью очищает фильмы, рейтинги, комментарии и пользователей (кроме admin).'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        with transaction.atomic():
            Rating.objects.all().delete()
            Comment.objects.all().delete()
            Movie.objects.all().delete()
            User.objects.exclude(username='admin').delete()
        self.stdout.write(self.style.SUCCESS(
            'База очищена, остался только admin, без фильмов!'))
