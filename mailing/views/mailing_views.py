from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views import generic
from mailing import models
from mailing import forms


class EditCheckMixin:
    # проверка пользователя на автора или суперюзера
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404('Изменять может только владелец')
        return self.object


class SetUserMixin:
    # заполнение поля 'user' модели текущим пользователем
    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PermissionAndLoginRequiredMixin(PermissionRequiredMixin, LoginRequiredMixin):
    model = models.Mailing


class MailingCreateView(PermissionRequiredMixin, SetUserMixin, generic.CreateView):
    permission_required = 'mailing.add_mailing'
    form_class = forms.MailingForm
    template_name = 'mailing/form.html'

    success_url = reverse_lazy('mailing:mailings')
    extra_context = {
        'title': 'Создание рассылки'
    }


class MailingsView(generic.ListView):
    model = models.Mailing
    template_name = 'mailing/mailings_list.html'
    extra_context = {
        'title': 'Рассылки',
    }


class MailingDeleteView(PermissionAndLoginRequiredMixin, EditCheckMixin, generic.DeleteView):
    permission_required = 'mailing.delete_mailing'
    success_url = reverse_lazy('mailing:mailings')
    template_name = 'mailing/confirm_delete.html'
    extra_context = {
        'title': 'Удалить рассылку'
    }


class MailingUpdateView(PermissionAndLoginRequiredMixin, EditCheckMixin, generic.UpdateView):
    permission_required = 'mailing.change_mailing'
    form_class = forms.MailingForm
    template_name = 'mailing/form.html'
    extra_context = {
        'title': 'Изменить данные рассылки'
    }

    def get_success_url(self):
        return reverse('mailing:mailings')
