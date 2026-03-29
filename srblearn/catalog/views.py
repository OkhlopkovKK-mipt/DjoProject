from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, WordAddForm
from .models import WordsData, WordTranslation
# from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def words_adding_view(request):
    if request.method == 'POST':
        form = WordAddForm(request.POST, request.FILES)
        if form.is_valid():
            original = form.cleaned_data['original']
            translation = form.cleaned_data['translation']
            image = form.cleaned_data.get('image')

            # Проверяем, существует ли слово
            word, created = WordsData.objects.get_or_create(
                original=original,
                defaults={'user': request.user, 'image': image}
            )
            if not created and image:
                # Если слово уже было, но пользователь загрузил новую картинку — обновим
                word.image = image
                word.save()

            # Проверяем, существует ли перевод
            translation_exists = WordTranslation.objects.filter(word=word, translated=translation).exists()
            if translation_exists:
                messages.error(request, f'Слово "{original}" с переводом "{translation}" уже существует.')
            else:
                # Добавляем новый перевод
                WordTranslation.objects.create(word=word, translated=translation)
                messages.success(request, f'Слово "{original}" успешно добавлено с переводом "{translation}".')
            return redirect('words_adding')
    else:
        form = WordAddForm()
    return render(request, 'words_adding.html', {'form': form})