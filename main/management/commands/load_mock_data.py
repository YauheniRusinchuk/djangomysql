from django.core.management.base import BaseCommand
from main.models import Movie
from datetime import date


class Command(BaseCommand):
    help = 'Loads mock movie data into the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Movie.objects.all().delete()
        self.stdout.write('Cleared existing movie data')

        # Mock data
        mock_movies = [
            {
                'title': 'Начало',
                'description': 'Профессиональный вор проникает в сны людей, чтобы украсть их секреты. Однажды ему поручают внедрить идею в подсознание жертвы.',
                'release_date': date(2010, 7, 16),
                'poster': 'https://api.kinoart.ru/storage/post/1837/regular_detail_picture-ab7f26934ed332effee4751621774bd3.jpg'
            },
            {
                'title': 'Матрица',
                'description': 'Хакер Нео узнаёт, что его мир — иллюзия, созданная машинами для порабощения человечества.',
                'release_date': date(1999, 3, 31),
                'poster': 'https://iy.kommersant.ru/Issues.photo/LifeStyle_Online/2019/03/29/KMO_111307_24478_1_t218_122831.jpg'
            },
            {
                'title': 'Интерстеллар',
                'description': 'Группа исследователей отправляется через червоточину в космосе, чтобы спасти человечество.',
                'release_date': date(2014, 11, 7),
                'poster': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJAFRW58lqpxxECGISs3F7ILV7f-y8iEgUyw&s'
            },
            {
                'title': '1+1 (Неприкасаемые)',
                'description': 'История дружбы парализованного аристократа и его помощника из бедного района.',
                'release_date': date(2011, 11, 2),
                'poster': 'https://lh4.googleusercontent.com/proxy/Qj-y3QOvs-PY0gNJSj4QOwVNZWFasWuHH_k_It5dx5G5JdFooaV0gv9Q18mfHyn07MDSURs218AmGYTT7OL6TAJ5G0AX4xLQ3hp7FRvLLpuyGKqg4CZY4vp4Gg'
            },
            {
                'title': 'Зеленая миля',
                'description': 'Охранник тюрьмы сталкивается с чудесными способностями заключённого, ожидающего смертной казни.',
                'release_date': date(1999, 12, 10),
                'poster': 'https://static.tildacdn.com/tild3661-6433-4862-a431-313263363632/zelenaya_milya_psiho.jpg'
            },
            {
                'title': 'Форрест Гамп',
                'description': 'Жизнь простого, но доброго человека, который становится свидетелем и участником важных событий в истории США.',
                'release_date': date(1994, 7, 6),
                'poster': 'https://cdn.maximonline.ru/3a/1f/63/3a1f63a15eaff691eb3f0fe49c944155/665x460_0xac120005_17195470731529055214.jpg'
            },
            {
                'title': 'Побег из Шоушенка',
                'description': 'Банкир, несправедливо осуждённый за убийство, не теряет надежды и планирует побег из тюрьмы.',
                'release_date': date(1994, 9, 23),
                'poster': 'https://avatars.mds.yandex.net/get-kinopoisk-post-img/1539913/e6dd24cbe07ab6ecd0d31dedd58b870f/960x540'
            },
        ]

        # Create movies
        for movie_data in mock_movies:
            Movie.objects.create(**movie_data)
            self.stdout.write(f'Created movie: {movie_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded mock data'))
