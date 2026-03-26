from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', max_length=30, help_text='Представьтесь (до 30 знаков).')
    email = forms.EmailField(label='Email', max_length=254, help_text='Введите действующий email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 30
        self.fields['username'].help_text = (
            'Представьтесь. Не более 30 символов. Только буквы, цифры и символы @/./+/-/_'
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)