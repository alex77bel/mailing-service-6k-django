
from django.views import generic

from mailing.models import MailingLogs


class MailingAttemptsView(generic.ListView):
    model = MailingLogs
    template_name = 'mailing/mailing_attempts.html'
    extra_context = {
        'title': 'Завершенные рассылки'
    }