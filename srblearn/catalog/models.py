from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    # 'username'
    # 'email'
    # 'password'
    answer_rate = models.IntegerField(default=0, verbose_name='Рейтинг ответов')

    class Meta:
        db_table = 'users_data'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class WordsData(models.Model):
    word_id = models.AutoField(primary_key=True)
    original = models.CharField(max_length=255, unique=True, verbose_name='Слово на сербском')
    image = models.ImageField(upload_to='words_images/', blank=True, null=True, verbose_name='Изображение слова')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        db_table = 'words_data'
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'

    def __str__(self):
        return self.original

class WordTranslation(models.Model):
    translation_id = models.AutoField(primary_key=True)
    word = models.ForeignKey(WordsData, on_delete=models.CASCADE, verbose_name='Слово')
    translated = models.CharField(max_length=255, verbose_name='Перевод')

    class Meta:
        db_table = 'word_translation'
        verbose_name = 'Перевод слова'
        verbose_name_plural = 'Переводы слов'

    def __str__(self):
        return f"{self.word.original} -> {self.translated}"