from django.apps import AppConfig
from jobs import updater

class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    # def ready(self):
    #     pass
    #     updater.start()