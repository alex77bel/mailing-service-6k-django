from smtplib import SMTPException

from django.core.mail import send_mail

from config import settings


def sendmail(message, recipient, subject='Рассылка Django'):  # отправка письма
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)
    except SMTPException as err:  # ошибка SMTP
        print('There was an error sending an email.' + err)
    except:  # другие ошибки
        print("Mail Sending Failed")


    # print(subject,'/', message,'/', settings.EMAIL_HOST_USER,'/', recipient)
    # print('отправка')


