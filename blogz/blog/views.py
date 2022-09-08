from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    DetailView,
    ListView
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from .models import Post
from .forms import PostAddForm, PostEditForm


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'


# This view should be based on the ListView class.
# The queryset has to accept posts that are filtered out
# by category.
# Something similar to this:
#
# # class PostsByCategoryView(ListView):
# #     model = Post
# #     template_name = 'blog/posts_by_category.html'
# #
# #     def get_queryset(self):
# #         qs = super().get_queryset()
# #         return qs.filter(category=category_id)
def posts_by_category(request, category):
    posts_list = Post.objects.filter(category=category)
    context = {
        'posts_list': posts_list,
        'category_name': category
    }
    return render(
        request,
        'blog/index.html',
        context
    )


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'owner']


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'owner']


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:profile')


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

# This view should be a ListView based view.
# Queryset has to accept posts filtered out by owner
# where the owner is a current logged-in user.
@login_required
def profile(request):
    # user = User.objects.get(username=request.user.username)
    # user_posts = Post.objects.filter(owner=user)
    # context = {
    #     'user_posts': user_posts
    # }
    return render(request, 'registration/profile.html', {})
