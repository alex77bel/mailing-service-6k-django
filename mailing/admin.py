from django.contrib import admin
from mailing.models import Client, Message, Mailing, MailingLogs, Post


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment', 'user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'user')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'date', 'time', 'frequency', 'status', 'message', 'user')


@admin.register(MailingLogs)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_request')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'published', 'views')
