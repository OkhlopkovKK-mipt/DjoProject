from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

class SignUpForm(UserCreationForm):
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
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)