from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import ModelFormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.views.generic import (
    DetailView,
    ListView
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CommentForm


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3


class PostsByCategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3

    # Redefine parent function to filter out queryset
    # by category_id attribute.
    def get_queryset(self):
        qs = super().get_queryset()
        # When we clicked on the category link, i.e. "Культура"
        # we're redirected to the URL http(s)://example.com/category/7
        # Thus, to get a category_id only what we need is to
        # split the url string from the 'path_info' and grub
        # the last element of the received list.
        category_id = str(self.request.path_info).split('/')[-1]
        return qs.filter(category=category_id)


class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentFormView.as_view()
        return view(request, *args, **kwargs)


class PostDetailView(SingleObjectMixin, TemplateResponseMixin, View):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['form'] = CommentForm()
        # We have to receive a list of comments
        # We can't use MultipleObjectMixin
        return self.render_to_response(context)


class CommentFormView(ModelFormMixin, View):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post_id})


def post_detail_view(request, pk):
    context = {}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:post_detail', kwargs={'pk': pk}))
    else:
        post = get_object_or_404(Post, pk=pk)
        comment_list = Comment.objects.filter(post=post.pk)
        # add user to the owner field
        form = CommentForm()
        context.update(
            {'post': post, 'form': form, 'comment_list': comment_list}
        )
        return render(request, 'blog/post_detail.html', context)


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category']
    success_url = reverse_lazy('blog:profile')
    template_name = 'blog/post_form.html'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'owner']
    success_url = reverse_lazy('blog:profile')
    template_name = 'blog/post_form.html'


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:profile')
    template_name = 'blog/post_confirm_delete.html'


def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:login'))
    else:
        form = UserCreationForm()
    return render(
        request,
        'registration/registration.html',
        {'form': form}
    )


class ProfileView(ListView):
    model = Post
    template_name = 'registration/profile.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = User.objects.get(username=self.request.user.username)
        return qs.filter(owner=user_id)
