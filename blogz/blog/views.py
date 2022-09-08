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
    paginate_by = 3


class PostsByCategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'

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


class ProfileView(ListView):
    model = Post
    template_name = 'registration/profile.html'

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = User.objects.get(username=self.request.user.username)
        return qs.filter(owner=user_id)
