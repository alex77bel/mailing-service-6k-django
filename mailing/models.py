from django.db import models


class Client(models.Model):
    # Клиент сервиса: контактный email, фио, комментарий
    name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'Клиент: {self.name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)


class Message(models.Model):
    # Сообщение для рассылки (тема письма, тело письма)

    title = models.CharField(max_length=250, verbose_name='Тема')
    body = models.TextField(verbose_name='Сообщение', default=None)

    def __str__(self):
        return f'Тема сообщения: {self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('title',)


class Mailing(models.Model):
    # Рассылка: время рассылки, периодичность, статус рассылки

    class Status(models.TextChoices):  # статус рассылки (завершена, создана, запущена)
        COMPLETED = 'CM', 'Completed'  # устанавливается после завершения
        CREATED = 'CR', 'Created'  # устанавливается после создания
        LAUNCHED = 'LA', 'Launched'  # устанавливается при запуске

    class Frequency(models.TextChoices):  # периодичность (раз в день, раз в неделю, раз в месяц)
        ONCE_A_DAY = 'DA', 'Once a day'
        ONCE_A_WEEK = 'WE', 'Once a week'
        ONCE_A_MONTH = 'MO', 'Once a month'

    time = models.TimeField(verbose_name='Время начала рассылки (ч:м:с)', null=False, blank=False)
    frequency = models.CharField(max_length=2,
                                 choices=Frequency.choices,
                                 default=Frequency.ONCE_A_DAY,
                                 verbose_name='Периодичность рассылки'
                                 )
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.CREATED,
                              verbose_name='Статус рассылки'
                              )
    # связи:
    # с Клиентами - многие ко многим (в рассылку могут входить несколько клиентов, клиент может быть в разных рассылках)
    # и Сообщениями - один ко многим (сообщение может входить во много рассылок, в рассылке - одно сообщение)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение', null=False, blank=False)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', blank=True)

    def __str__(self):
        return f'Рассылка в: {self.time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('-time',)


class MailingAttempt(models.Model):
    # Попытка рассылки (дата и время последней попытки, статус попытки, ответ почтового сервера)

    class Status(models.TextChoices):  # статус (активная, завершенная)
        ACTIVE = 'AC', 'Active'
        COMPLETED = 'CO', 'Completed'

    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.ACTIVE,
                              verbose_name='Статус попытки рассылки'
                              )
    server_request = models.CharField(max_length=250)
    # связь с Рассылкой - один ко многим (у рассылки может быть несколько попыток, по расписанию)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True)

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, verbose_name='Слаг', unique_for_date='created')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(verbose_name='Признак публикации', default=False)
    views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)

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
