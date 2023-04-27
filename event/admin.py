from django.contrib import admin
from .models import Event
from .models import Users
from .models import UsersEvents



class EvAdmin(admin.ModelAdmin):
    list_display = ('name', 'desctiption', 'logo', 'status_event', 'data_start', 'data_end', 'city')
    list_display_links = ('name', 'desctiption', 'logo', 'status_event', 'data_start', 'data_end', 'city')
    search_fields = ('name', 'desctiption', 'logo', 'status_event', 'data_start', 'data_end', 'city')


admin.site.register(Event, EvAdmin)
admin.site.register(Users)
admin.site.register(UsersEvents)



#class UsAdmin(admin.ModelAdmin):
#    list_display = ('last_name', 'first_name', 'age', 'city')
#    list_display_links = ('last_name', 'first_name')
#    search_fields = ('last_name', 'first_name',)


#admin.site.register(Event, EvAdmin)
#admin.site.register(User, UsAdmin)


# class User(models.Model):
#     last_name = models.CharField(max_length=50, verbose_name='Фамилия')
#     first_name = models.CharField(max_length=50, verbose_name='Имя')
#     age = models.FloatField(null=True, blank=True, verbose_name='Возраст')
#     city = models.CharField(max_length=50, verbose_name='Город')
#     sex = models.CharField(max_length=4, verbose_name='Пол')
#     email = models.EmailField(max_length=50, verbose_name='Почта')
#     password = models.CharField(max_length=50, verbose_name='Пароль')
#
#
# class Event(models.Model):
#     desctiption = models.TextField(null=True, blank=True, verbose_name='Описание')
#     title = models.CharField(max_length=50, verbose_name='Заголовок')
#     type = models.BooleanField(verbose_name='Тип')
#     logo = models.ImageField(max_length=50, verbose_name='Логотип')
#     data_event = models.DateField(null=True, verbose_name='Дата')
#     duration = models.IntegerField(null=True, blank=True, verbose_name='Длина')
#     city = models.TextField(max_length=50, verbose_name='Город')

# class BbAdmin(admin.ModelAdmin):
#     list_display = ('title', 'content', 'prise', 'published','rubric')
#     list_display_links = ('title', 'content')
#     search_fields = ('title', 'content',)
#
#
# admin.site.register(Bb, BbAdmin)