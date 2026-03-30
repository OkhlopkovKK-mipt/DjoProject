"""
Forms for user registration, authentication, and word management.

Includes custom sign-up form, login form, and a form for adding words
with validation for Serbian and Russian letters.
"""

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.validators import RegexValidator

LETTERS_PATTERN = r'^[a-zA-Zа-яА-ЯёЁ\u0400-\u04FFčćđšžČĆĐŠŽ\-]+$'

class SignUpForm(UserCreationForm):
    """Custom sign-up form with an email field and custom username help text."""

    email = forms.EmailField(label='Email', max_length=254, help_text='Введите действующий email.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 30
        self.fields['username'].help_text = (
            'Представьтесь. Не более 30 символов. Только буквы, цифры и символы @/./+/-/_'
        )

class LoginForm(AuthenticationForm):
    """Custom login form with username and password fields."""

    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class WordAddForm(forms.Form):
    """Form for adding a Serbian word, its translation, and an optional image."""

    original = forms.CharField(
        label='Сербское слово',
        max_length=255,
        validators=[
            RegexValidator(
                regex=LETTERS_PATTERN,
                message='Слово должно содержать только буквы и дефис.',
                code='invalid_word'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    translation = forms.CharField(
        label='Перевод',
        max_length=255,
        validators=[
            RegexValidator(
                regex=LETTERS_PATTERN,
                message='Слово должно содержать только буквы и дефис.',
                code='invalid_word'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Картинка (необязательно)',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
