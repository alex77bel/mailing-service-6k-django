from django.contrib.auth import mixins
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import generic

from mailing.forms import BlogForm
from mailing.models import Post


class BlogPostCreateView(mixins.PermissionRequiredMixin, generic.CreateView):
    permission_required = 'mailing.add_post'
    model = Post
    form_class = BlogForm
    template_name = 'mailing/form.html'
    success_url = reverse_lazy('mailing:blog')
    extra_context = {
        'title': 'Создание статьи'
    }

    def form_valid(self, form):
        if form.is_valid:
            fields = form.save(commit=False)
            string = fields.title.translate(
                str.maketrans("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                              "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
            fields.slug = slugify(string)
            fields.save()
        return super().form_valid(form)


class BlogView(generic.ListView):
    model = Post
    template_name = 'mailing/blog.html'
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        return queryset


class BlogPostDetailView(generic.DetailView):
    model = Post

    def get_object(self, queryset=None):  # добавление одного просмотра
        post = super().get_object()
        post.add_view()
        post.save()
        return post

    def get_context_data(self, **kwargs):  # получение 'title'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Просмотр статьи'
        return context_data


class BlogPostUpdateView(mixins.PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'mailing.change_post'
    model = Post
    form_class = BlogForm
    template_name = 'mailing/form.html'

    extra_context = {
        'title': 'Изменить статью'
    }

    def get_success_url(self):
        return reverse('mailing:post', args=[*self.kwargs.values()])


class BlogPostDeleteView(mixins.PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'mailing.delete_post'
    model = Post
    template_name = 'mailing/confirm_delete.html'
    extra_context = {
        'title': 'Удаление'
    }
    success_url = reverse_lazy('mailing:blog')
