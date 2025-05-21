from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.db import transaction
from django.contrib.auth import get_user_model

# модели в БД


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField(default=datetime.date(2000, 1, 1))
    poster = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Добавил')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            self.average_rating = sum(r.rating for r in ratings) / len(ratings)
        else:
            self.average_rating = 0
        self.save()


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_average_rating()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"


class Comment(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return f"{self.name} ({self.email})"


# --- Моковые данные ---
def create_mock_movies():
    pass


def recreate_mock_movies():
    with transaction.atomic():
        Movie.objects.all().delete()
        create_mock_movies()
