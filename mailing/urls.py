from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import client_views, message_views, mailing_views, blog_views, main_views, mailing_attempts_views

app_name = MailingConfig.name

urlpatterns = [
    path('', main_views.MainView.as_view(), name='main'),

    path('clients/', client_views.ClientsView.as_view(), name='clients'),
    path('clients/create/', client_views.ClientCreateView.as_view(), name='create_client'),
    path('clients/update/<int:pk>', client_views.ClientUpdateView.as_view(), name='update_client'),
    path('clients/delete/<int:pk>', client_views.ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', message_views.MessagesView.as_view(), name='messages'),
    path('messages/create/', message_views.MessageCreateView.as_view(), name='create_message'),
    path('messages/update/<int:pk>', message_views.MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>', message_views.MessageDeleteView.as_view(), name='delete_message'),

    path('mailings/', mailing_views.MailingsView.as_view(), name='mailings'),
    path('mailings/create/', mailing_views.MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/update/<int:pk>', mailing_views.MailingUpdateView.as_view(), name='update_mailing'),
    path('mailings/delete/<int:pk>', mailing_views.MailingDeleteView.as_view(), name='delete_mailing'),

    path('mailing_attempts/', mailing_attempts_views.MailingAttemptsView.as_view(), name='mailing_attempts'),

    path('blog/', cache_page(60)(blog_views.BlogView.as_view()), name='blog'),
    path('blog/create_post/', blog_views.BlogPostCreateView.as_view(), name='create_post'),
    path('blog/post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         cache_page(60)(blog_views.BlogPostDetailView.as_view()), name='post'),
    path('blog/update_post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         blog_views.BlogPostUpdateView.as_view(), name='update_post', ),
    path('blog/delete_post/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         blog_views.BlogPostDeleteView.as_view(), name='delete_post'),

]
