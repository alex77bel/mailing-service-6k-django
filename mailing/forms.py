from django import forms
from mailing import models


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ('name', 'email', 'comment')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('title', 'body')

class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Mailing
        fields = ('time', 'frequency', 'clients', 'message')


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'content', 'preview', 'published')
