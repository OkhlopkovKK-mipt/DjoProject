from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, WordAddForm
from .models import WordsData, WordTranslation
from django.contrib.auth import get_user_model
import random
from django.db.models import Prefetch
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

            # Checking the existence of the word in db
            word, created = WordsData.objects.get_or_create(
                original=original,
                defaults={'user': request.user, 'image': image}
            )
            if not created and image:
                # If there are word and translation, but there is new picture, it will be updated
                word.image = image
                word.save()

            # Checking the existence of translation in db
            translation_exists = WordTranslation.objects.filter(word=word, translated=translation).exists()
            if translation_exists:
                messages.error(request, f'Слово "{original}" с переводом "{translation}" уже существует,'
                                        f'меняется только картинка.')
            else:
                # Adding new translation
                WordTranslation.objects.create(word=word, translated=translation)
                messages.success(request, f'Слово "{original}" успешно добавлено с переводом "{translation}".')
            return redirect('words_adding')
    else:
        form = WordAddForm()
    return render(request, 'words_adding.html', {'form': form})

def words_list_view(request):
    words = WordsData.objects.prefetch_related('wordtranslation_set').all()

    context = {
        'words': words,
    }
    return render(request, 'words_list.html', context)


@login_required
def rating_view(request):
    # Top-5 users by answer_rate (descending)
    top_users = get_user_model().objects.order_by('-answer_rate')[:5]

    # Current user rating position
    current_user_rank = get_user_model().objects.filter(
        answer_rate__gt=request.user.answer_rate
    ).count() + 1

    # Checking if user is in top-5
    current_user_in_top = request.user in top_users

    context = {
        'top_users': top_users,
        'current_user': request.user,
        'current_user_rank': current_user_rank,
        'current_user_in_top': current_user_in_top,
    }
    return render(request, 'users_rating.html', context)


@login_required
def quiz_view(request):
    # Checking for existence of words in db
    all_words = WordsData.objects.all()

    if not all_words.exists():
        messages.warning(request, 'Сначала добавьте слова для прохождения квиза!')
        return redirect('words_adding')

    # Checking the answer
    if request.method == 'POST':
        word_id = request.POST.get('word_id')
        user_answer = request.POST.get('answer', '').strip().lower()

        if word_id:
            # Getting the word
            word = get_object_or_404(WordsData, word_id=word_id)

            # Getting all correct translations
            correct_translations = WordTranslation.objects.filter(word=word)
            correct_answers = [t.translated.lower().strip() for t in correct_translations]

            # Is answer correct
            if user_answer in correct_answers:
                # OK +1 point
                request.user.answer_rate += 1
                request.user.save()
                messages.success(request, f'Правильно! +1 балл (Ответ: {correct_translations.first().translated})')
            else:
                # Fail -1 point
                request.user.answer_rate -= 1
                request.user.save()
                messages.error(request,
                               f'Неправильно! -1 балл (Правильный ответ: {correct_translations.first().translated})')

        # Redirect to the same page (GET request) with a new word
        return redirect('quiz')

    # If GET request, a random word is displayed
    random_word = random.choice(list(all_words))

    context = {
        'word': random_word,
        'total_words': all_words.count(),
    }
    return render(request, 'quiz.html', context)
