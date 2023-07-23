import datetime
from smtplib import SMTPException

from django.core.cache import cache
from django.core.mail import send_mail

from config import settings
from mailing.models import Mailing, MailingLogs, Post


def get_posts_cached(n: int):  # получает n случайных статей и хранит их в кэше
    if settings.CACHE_ENABLED:  # если кэш включен
        key = 'posts'
        posts = cache.get(key)  # ищем нужный ключ
        if posts is None:  # если не нашли
            posts = Post.objects.all()  # берем из бд
            cache.set(key, posts)  # и кэшируем
    else:
        posts = Post.objects.all()  # если кэш отключен, берем из бд
    return posts.order_by('?')[:n]


def sendmail(message, recipient, subject='Рассылка Django'):  # отправка письма
    status = False
    try:
        response = send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
        status = True
    except SMTPException as err:  # ошибка SMTP
        response = 'Произошла ошибка при отправке письма' + str(err)
    except:  # другие ошибки
        response = "Отправка почты не удалась"
    return status, response


def mailing_processing():
    mailing_duration = datetime.timedelta(minutes=5)  # время активности рассылки, минут

    def check_mailing_time_is_running():  # проверка времени активности рассылки
        delta = datetime.datetime.now() - datetime.datetime.combine(mailing.date, mailing.time)
        return datetime.timedelta() < delta <= mailing_duration

    for mailing in Mailing.objects.all():
        if mailing.is_active:  # если рассылка разрешена
            if mailing.status == 'CR':  # статус рассылки - создана, надо проверить необходимость отправки
                if check_mailing_time_is_running():  # если наступило время рассылки
                    mailing.status = 'LA'  # статус рассылки - запущена
                    mailing.save()
                    mailing_attempt = sendmail(mailing.message.body,
                                               [client.email for client in mailing.clients.all()])  # запуск рассылки
                    server_request = str(mailing) + \
                                     ', прошла успешно' if mailing_attempt[0] \
                        else f', прошла c ошибками {mailing_attempt[1]}'
                    MailingLogs.objects.create(time=datetime.datetime.now(),
                                               status=mailing_attempt[0],
                                               server_request=server_request)
                    mailing.status = 'CM'  # статус рассылки - завершена
                    mailing.save()

            elif mailing.status == 'CM':  # статус рассылки - завершена, надо проверить необходимость сброса статуса
                if not check_mailing_time_is_running():  # если время рассылки закончилось
                    mailing.status = 'CR'  # сброс статуса
                    # установка даты следующего запуска рассылки
                    match mailing.frequency:
                        case 'DA':
                            mailing.date += datetime.timedelta(days=1)
                        case 'WE':
                            mailing.date += datetime.timedelta(days=7)
                        case 'MO':
                            mailing.date += datetime.timedelta(days=30)
                    mailing.save()
