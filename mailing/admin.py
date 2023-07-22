from django.contrib import admin
from mailing.models import Client, Message, Mailing, MailingLogs, Post


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'frequency', 'status', 'message')

@admin.register(MailingLogs)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_request')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'published', 'views')
