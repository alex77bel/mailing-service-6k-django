from django.urls import reverse_lazy, reverse
from django.views import generic

from mailing.forms import ClientForm
from mailing.models import Client


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/form.html'
    # fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('mailing:clients')
    extra_context = {
        'title': 'Создание клиента рассылки'
    }


class ClientsView(generic.ListView):
    model = Client
    template_name = 'mailing/clients_list.html'
    extra_context = {
        'title': 'Клиенты для рассылки'
    }


class ClientDeleteView(generic.DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')
    template_name = 'mailing/confirm_delete.html'
    extra_context = {
        'title': 'Удалить клиента'
    }


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    # fields = ('name', 'email', 'comment')
    template_name = 'mailing/form.html'
    extra_context = {
        'title': 'Изменить данные клиента'
    }

    def get_success_url(self):
        return reverse('mailing:clients')
