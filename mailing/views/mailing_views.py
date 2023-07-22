from django.urls import reverse_lazy, reverse
from django.views import generic
from mailing import models
from mailing import forms


class MailingCreateView(generic.CreateView):
    model = models.Mailing
    form_class = forms.MailingForm
    # fields = ('time', 'frequency', 'clients', 'message')
    template_name = 'mailing/form.html'

    success_url = reverse_lazy('mailing:mailings')
    extra_context = {
        'title': 'Создание рассылки'
    }

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     if form.is_valid():
    #         fields = form.save()
    #         # print(fields.time, fields.frequency, fields.clients, fields.message)


        # return super().form_valid(form)




class MailingsView(generic.ListView):
    model = models.Mailing
    template_name = 'mailing/mailings_list.html'
    extra_context = {
        'title': 'Рассылки',
    }
    # print(Mailing.objects.values('id','clients'))
    # q = Mailing.objects.get(id='3').clients.all()
    # for i in q:
    #     print(i.name)
    # print(q)



class MailingDeleteView(generic.DeleteView):
    model = models.Mailing
    success_url = reverse_lazy('mailing:mailings')
    template_name = 'mailing/confirm_delete.html'
    extra_context = {
        'title': 'Удалить рассылку'
    }


class MailingUpdateView(generic.UpdateView):
    model = models.Mailing
    form_class = forms.MailingForm
    # fields = ('time', 'frequency', 'status', 'clients', 'message')
    template_name = 'mailing/form.html'
    extra_context = {
        'title': 'Изменить данные рассылки'
    }

    # q = models.Client.objects.get(name='Александр1')
    # print(q.mailing_set.all())

    def get_success_url(self):
        return reverse('mailing:mailings')
