from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import User


class Client(models.Model):
    # Клиент сервиса

    name = models.CharField(max_length=100,
                            verbose_name='ФИО')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', null=True)

    def __str__(self):
        return f'Клиент: {self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)


class Message(models.Model):
    # Сообщение для рассылки

    title = models.CharField(max_length=250,
                             verbose_name='Тема')
    body = models.TextField(default=None,
                            verbose_name='Сообщение')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', null=True)

    def __str__(self):
        return f'Тема сообщения: {self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    # Рассылка

    class Status(models.TextChoices):  # подкласс для выбора статуса рассылки
        COMPLETED = 'CM', 'completed'  # устанавливается после завершения
        CREATED = 'CR', 'created'  # устанавливается после создания
        LAUNCHED = 'LA', 'launched'  # устанавливается при запуске

    class Frequency(models.TextChoices):  # подкласс для выбора периодичности
        ONCE_A_DAY = 'DA', 'ежедневно'
        ONCE_A_WEEK = 'WE', 'еженедельно'
        ONCE_A_MONTH = 'MO', 'ежемесячно'

    time = models.TimeField(default=timezone.now,
                            verbose_name='Время начала рассылки, (чч:мм:сс)')
    date = models.DateField(default=timezone.now,
                            verbose_name='Дата следующей рассылки, (дд.мм.гггг)')
    frequency = models.CharField(max_length=2,
                                 choices=Frequency.choices,
                                 default=Frequency.ONCE_A_DAY,
                                 verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=2,  # статус
                              choices=Status.choices,
                              default=Status.CREATED,
                              verbose_name='Статус рассылки')
    is_active = models.BooleanField(default=True, verbose_name='Разрешение рассылки')
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                verbose_name='Сообщение')
    clients = models.ManyToManyField(Client,
                                     verbose_name='Клиенты',
                                     related_name='mailing')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец', null=True)

    def get_label(self, frequency):
        for label in self.Frequency.choices:
            if label[0] == frequency: return label[1]

    def __str__(self):
        return f'Рассылка в {self.time} с {self.date.strftime("%d.%m.%Y")}, {self.get_label(self.frequency)}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('-time',)


class MailingLogs(models.Model):
    # Лог попытки рассылки

    time = models.DateTimeField(verbose_name='Дата и время последней рассылки')
    status = models.BooleanField()
    server_request = models.CharField(max_length=250,
                                      verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ('-time',)


class Post(models.Model):
    # Статья блога

    title = models.CharField(max_length=255,
                             verbose_name='Заголовок')
    slug = models.CharField(max_length=255,
                            unique_for_date='created',
                            verbose_name='Слаг')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/',
                                verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    published = models.BooleanField(default=False,
                                    verbose_name='Признак публикации')
    views = models.PositiveIntegerField(default=0,
                                        verbose_name='Количество просмотров')

    def add_view(self):
        self.views += 1
        return self.views

    def delete(self, *args, **kwargs):
        self.published = False
        self.save()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-created',)
