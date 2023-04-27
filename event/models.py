from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Users(models.Model):
    MAN = 'M'
    WOMAN = 'W'
    SEX = [
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    second_name = models.CharField(max_length=50, verbose_name='Отчество', help_text='Отчество пользователя')
    age = models.IntegerField(null=True, verbose_name='Возраст', help_text='Полных лет пользователя')
    city = models.CharField(max_length=50, verbose_name='Город', help_text='Город, в котором живет пользователь')
    sex = models.CharField(max_length=1, choices=SEX, default=MAN, help_text='Пол пользователя')

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'


class Event(models.Model):
    DONTSTART = '1'
    STARTING = '2'
    END = '3'
    STATUS_EVENT = [
        (DONTSTART, 'Не началось'),
        (STARTING, 'В процессе'),
        (END, 'Закончилось'),
    ]
    name = models.CharField(max_length=50, verbose_name='Название', help_text='Название мероприятия')
    desctiption = models.TextField(null=True, blank=True, verbose_name='Описание', help_text='Описание мероприятия')
    logo = models.ImageField(max_length=50, verbose_name='Логотип', help_text='Логотип мероприятия', upload_to='images/')
    status_event = models.CharField(max_length=1, choices=STATUS_EVENT, default=DONTSTART, help_text='Статус мероприятия')
    data_start = models.DateField(null=True, verbose_name='Дата начала', help_text='Дата начала мероприятия')
    data_end = models.DateField(null=True, verbose_name='Дата конца', help_text='Дата конца мероприятия')
    city = models.TextField(max_length=50, verbose_name='Город', help_text='Город проведения мероприятия')

    class Meta:
        verbose_name_plural = 'События'
        verbose_name = 'Событие'
        ordering = ['-status_event', '-data_start', '-data_end']


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Роль', help_text='Роль человека на мероприятии')

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class UsersEvents(models.Model):
    id_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_reg = models.DateField(null=True, verbose_name='Дата регистрации', help_text='Дата регистрации на меропрятии')
    link_certificate = models.FileField(null=True, verbose_name='Сертификат', help_text='Сертификат участника мероприятия')
    rating = models.IntegerField(null=True, verbose_name='Занимеемое место', help_text='Занимеемое место на мероприятии')

    class Meta:
        verbose_name_plural = 'События и участники'
        verbose_name = 'Событие и участник'
        ordering = ['-id_status', '-date_reg', '-rating']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.users.save()
