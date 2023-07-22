from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from mailing.forms import MessageForm
from mailing.models import Message
from mailing.views.mailing_views import SetUserMixin, EditCheckMixin


class MessageCreateView(PermissionRequiredMixin, SetUserMixin, generic.CreateView):
    permission_required = 'mailing.add_message'
    form_class = MessageForm
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:messages')
    extra_context = {
        'title': 'Создание сообщения'
    }


class MessagesView(generic.ListView):
    model = Message
    template_name = 'mailing/messages_list.html'
    extra_context = {
        'title': 'Сообщения'
    }


class MessageDeleteView(PermissionRequiredMixin, EditCheckMixin, generic.DeleteView):
    permission_required = 'mailing.delete_mailing'
    model = Message
    success_url = reverse_lazy('mailing:messages')
    template_name = 'mailing/confirm_delete.html'
    extra_context = {
        'title': 'Удалить сообщение'
    }


class MessageUpdateView(PermissionRequiredMixin, EditCheckMixin, generic.UpdateView):
    permission_required = 'mailing.change_message'
    model = Message
    form_class = MessageForm
    template_name = 'mailing/form.html'
    extra_context = {
        'title': 'Изменить сообщение'
    }

    def get_success_url(self):
        return reverse('mailing:messages')
