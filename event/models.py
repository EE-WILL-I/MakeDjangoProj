from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Users(models.Model):
    MAN = 'M'
    WOMAN = 'W'
    AMERICAN = 'N'
    SEX = [
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
        (AMERICAN, 'Средний'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Логин пользователя')
    second_name = models.CharField(null=True, blank=True, max_length=50, verbose_name='Отчество', help_text='Отчество пользователя')
    age = models.IntegerField(null=True, verbose_name='Возраст', help_text='Полных лет пользователя')
    city = models.CharField(max_length=50, verbose_name='Город', help_text='Город, в котором живет пользователь')
    sex = models.CharField(max_length=1, verbose_name='Пол', choices=SEX, default=MAN, help_text='Пол пользователя')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['-id']


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Роль', help_text='Роль человека на мероприятии')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', help_text='Название мероприятия')
    description = models.TextField(null=True, blank=True, verbose_name='Описание', help_text='Описание мероприятия')
    logo = models.ImageField(null=True, blank=True, max_length=50, verbose_name='Логотип', help_text='Логотип мероприятия', upload_to='images/')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1, verbose_name='Статус', help_text='Статус мероприятия')
    data_start = models.DateField(verbose_name='Дата начала', help_text='Дата начала мероприятия')
    data_end = models.DateField(verbose_name='Дата конца', help_text='Дата конца мероприятия')
    city = models.CharField(max_length=80, verbose_name='Город', help_text='Город проведения мероприятия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='Создатель', help_text='Логин создателя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'
        ordering = ['-status', '-data_start', '-data_end']


class UserStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Роль', help_text='Статус на мероприятии')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class UsersEvents(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие в котором учавствует пользователь')
    users = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Логин пользователя')
    status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, default=1, null=True, verbose_name='Статус участника')
    date_reg = models.DateField(default=timezone.now, verbose_name='Дата регистрации', help_text='Дата регистрации на меропрятии')
    link_certificate = models.FileField(null=True, blank=True, verbose_name='Сертификат', help_text='Сертификат участника мероприятия', upload_to='files/')
    rating = models.IntegerField(null=True, blank=True, verbose_name='Занимеемое место', help_text='Занимеемое место на мероприятии')

    class Meta:
        verbose_name_plural = 'События и участники'
        verbose_name = 'Событие и участник'
        ordering = ['-status', '-date_reg', '-rating']
