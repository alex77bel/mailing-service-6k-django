from django.core.management import BaseCommand

from mailing.services import mailing_processing


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailing_processing()

