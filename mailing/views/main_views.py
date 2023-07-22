from django.views import generic

from mailing.models import Client, Mailing, Post


class MainView(generic.TemplateView):
    template_name = 'mailing/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['mailings_total'] = Mailing.objects.count()
        context['mailings_active'] = Mailing.objects.filter(is_active=True).count()
        unique_clients = []
        for client in Client.objects.all():
            if client.mailing.count() == 1:
                unique_clients.append(client.name)
        context['unique_clients'] = ', '.join(unique_clients)
        context['posts'] = Post.objects.order_by('?')[:3]

        return context
