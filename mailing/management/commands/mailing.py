import datetime
import time

from django.core.management import BaseCommand

from mailing.services import sendmail


class Command(BaseCommand):

    def handle(self, *args, **options):
        # while True:
        #     time.sleep(1)
        sendmail()
            # print(datetime.datetime.now())

