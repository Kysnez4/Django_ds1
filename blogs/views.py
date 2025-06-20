from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from blogs.forms import PostForm
from blogs.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blogs/blogs.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация по опубликованным статьям
        queryset = queryset.filter(publication=True)

        # Обработка поискового запроса
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(headline__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        session_key = f'post_viewed_{obj.pk}'

        # Проверяем, не просматривал ли пользователь пост ранее
        if not self.request.session.get(session_key, False):
            obj.views += 1
            obj.save()
            self.request.session[session_key] = True  # Помечаем как просмотренный

        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_update_form'
    enctype = 'multipart/form-data'

    def get_success_url(self):
        # Перенаправление на просмотр статьи после редактирования
        return reverse_lazy('blogs:post-detail', kwargs={'pk': self.object.pk})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_form.html'
    success_url = reverse_lazy('blogs:home')
    enctype = 'multipart/form-data'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:home')
    template_name = 'blogs/post_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Разрешаем удаление только для staff пользователей
        if not self.request.user.is_staff:
            return queryset.none()
        return queryset
