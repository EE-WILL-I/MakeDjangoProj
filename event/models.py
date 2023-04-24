from django.db import models

class User(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    age = models.FloatField(null=True, blank=True, verbose_name='Возраст')
    city = models.CharField(max_length=50, verbose_name='Город')
    sex = models.CharField(max_length=4, verbose_name='Пол')
    email = models.EmailField(max_length=50, verbose_name='Почта')
    password = models.CharField(max_length=50, verbose_name='Пароль')
    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['-last_name']


class Event(models.Model):
    desctiption = models.TextField(null=True, blank=True, verbose_name='Описание')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    type = models.BooleanField(verbose_name='Тип')
    logo = models.ImageField(max_length=50, verbose_name='Логотип')
    data_event = models.DateField(null=True, verbose_name='Дата')
    duration = models.IntegerField(null=True, blank=True, verbose_name='Длина')
    city = models.TextField(max_length=50, verbose_name='Город')
    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'
        ordering = ['-data_event']

