from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import DatabaseError
from django.db.utils import ProgrammingError
from django.core.paginator import Paginator
from .models import Movie, Comment, Rating, create_mock_movies
from .forms import UserRegistrationForm, UserLoginForm, CommentForm, RatingForm, MovieForm, FeedbackForm, UserEditForm


# view для обработки запросов на регистрацию и авторизацию и вывод списка фильмов


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('main:movie_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('main:movie_list')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('main:movie_list')


def movie_list(request):
    try:
        search_query = request.GET.get('search', '')
        movies = Movie.objects.all().order_by('-created_at')
        if search_query:
            movies = movies.filter(title__icontains=search_query)

        # Добавляем пагинацию
        paginator = Paginator(movies, 9)  # 9 фильмов на страницу
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'main/movie_list.html', {
            'movies': page_obj,
            'page_obj': page_obj,
            'search_query': search_query
        })
    except ProgrammingError:
        # Таблицы не созданы (нет миграций)
        return render(request, 'main/movie_list.html', {
            'movies': [],
            'db_error': True
        })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = movie.comments.all().order_by('-created_at')
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(
            movie=movie, user=request.user).first()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'comment' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.movie = movie
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'Комментарий успешно добавлен!')
                    return redirect('main:movie_detail', movie_id=movie.id)
            elif 'rating' in request.POST:
                rating_form = RatingForm(request.POST, instance=user_rating)
                if rating_form.is_valid():
                    rating = rating_form.save(commit=False)
                    rating.movie = movie
                    rating.user = request.user
                    rating.save()
                    movie.update_average_rating()
                    messages.success(request, 'Ваша оценка успешно сохранена!')
                    return redirect('main:movie_detail', movie_id=movie.id)
        else:
            messages.warning(
                request, 'Пожалуйста, войдите в систему, чтобы оставить комментарий или оценку.')
            return redirect('main:login')

    comment_form = CommentForm()
    rating_form = RatingForm(instance=user_rating)

    context = {
        'movie': movie,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating
    }
    return render(request, 'main/movie_detail.html', context)


@login_required
def add_comment(request, movie_id):
    try:
        movie = get_object_or_404(Movie, id=movie_id)
    except DatabaseError:
        messages.error(
            request, 'Не удалось загрузить фильм. Пожалуйста, попробуйте позже.')
        return redirect('main:movie_list')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
                comment.save()
                messages.success(request, 'Ваш комментарий добавлен.')
            except DatabaseError:
                messages.error(
                    request, 'Не удалось сохранить комментарий. Пожалуйста, попробуйте позже.')
    else:
        form = CommentForm()

    return redirect('main:movie_detail', movie_id=movie.id)


@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    user_rating = Rating.objects.filter(movie=movie, user=request.user).first()
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=user_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.user = request.user
            rating.save()
            movie.update_average_rating()
            messages.success(request, 'Ваша оценка успешно сохранена!')
        else:
            messages.error(request, 'Ошибка в оценке. Попробуйте ещё раз.')
    return redirect('main:movie_detail', movie_id=movie.id)


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            messages.success(request, 'Фильм успешно добавлен!')
            return redirect('main:movie_list')
    else:
        form = MovieForm()
    return render(request, 'main/add_movie.html', {'form': form})


@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.user != request.user:
        messages.error(request, 'Вы не являетесь автором этого фильма!')
        return redirect('main:movie_detail', movie_id=movie.id)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фильм успешно обновлён!')
            return redirect('main:movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'main/edit_movie.html', {'form': form, 'movie': movie})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('main:feedback')
    else:
        form = FeedbackForm()
    return render(request, 'main/feedback.html', {'form': form})


@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.user != request.user:
        messages.error(request, 'Вы не являетесь автором этого фильма!')
        return redirect('main:movie_detail', movie_id=movie.id)

    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Фильм успешно удалён!')
        return redirect('main:movie_list')

    return render(request, 'main/delete_movie.html', {'movie': movie})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
    else:
        form = UserEditForm(instance=user)
    movies = user.movie_set.all()
    return render(request, 'main/profile.html', {'form': form, 'movies': movies})
