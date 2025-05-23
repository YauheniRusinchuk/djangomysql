from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Comment, Rating, Movie, Feedback
from django.conf import settings


class CustomPasswordValidator:
    def __init__(self, password):
        self.password = password

    def validate(self):
        if self.password.isdigit():
            raise ValidationError(
                settings.PASSWORD_VALIDATION_MESSAGES['password_entirely_numeric']
            )
        if len(self.password) < 8:
            raise ValidationError(
                settings.PASSWORD_VALIDATION_MESSAGES['password_too_short']
            )
        if self.password.lower() in ['password', '12345678', 'qwerty123']:
            raise ValidationError(
                settings.PASSWORD_VALIDATION_MESSAGES['password_too_common']
            )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Почта'),
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите адрес почты'}),
        error_messages={
            'required': 'Пожалуйста, введите адрес почты',
            'invalid': 'Пожалуйста, введите корректный адрес почты',
            'unique': 'Этот адрес почты уже зарегистрирован'
        }
    )
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
        error_messages={
            'required': 'Пожалуйста, введите имя пользователя',
            'unique': 'Это имя пользователя уже занято',
            'invalid': 'Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_',
            'max_length': 'Имя пользователя не должно превышать 150 символов'
        }
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        help_text=_('Минимум 8 символов')
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        help_text=_('Введите тот же пароль, что и выше')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот адрес почты уже зарегистрирован')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'step': '1',
                'placeholder': 'Введите оценку (1-10)'
            })
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description',
                  'release_date', 'poster', 'video_url']
        labels = {
            'title': 'Название фильма',
            'description': 'Описание',
            'release_date': 'Дата выхода',
            'poster': 'URL постера',
            'video_url': 'URL видео',
        }
        help_texts = {
            'title': 'Введите название фильма',
            'description': 'Краткое описание фильма',
            'release_date': 'Укажите дату выхода фильма',
            'poster': 'Вставьте ссылку на постер (картинку)',
            'video_url': 'Вставьте ссылку на видео (YouTube, Vimeo и т.д.)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название фильма'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'дд.мм.гггг'}),
            'poster': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL постера'}),
            'video_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL видео'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        labels = {
            'name': 'Ваше имя',
            'email': 'Ваш email',
            'message': 'Сообщение',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите сообщение'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
