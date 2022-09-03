from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import\
    Post, \
    User
from .forms import \
    PostAddForm,\
    PostEditForm,\
    UserRegistrationForm,\
    UserAuthenticationForm


def index(request):
    now = timezone.now()
    posts_list = Post.objects.filter(publication_date__lte=now)
    context = {
        'posts_list': posts_list
    }
    return render(request, 'blog/index.html', context)


def posts_by_category(request, category_id):
    posts_list = Post.objects.filter(category=category_id)
    context = {
        'posts_list': posts_list,
        'category_name': category_id
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


def post_add(request):
    if request.method == 'POST':
        post_add_form = PostAddForm(request.POST)
        if post_add_form.is_valid():
            post_add_form.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        post_add_form = PostAddForm()
    return render(request, 'blog/post_add.html', {'post_add_form': post_add_form})


def post_edit(request, post_id):
    editing_post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post_edit_form = PostEditForm(request.POST)
        if post_edit_form.is_valid():
            # If a field is not changed don't rewrite it to the DB
            editing_post.title = request.POST['title']
            editing_post.content = request.POST['content']
            editing_post.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        post_edit_form = PostEditForm(instance=editing_post)
    return render(request, 'blog/post_edit.html', {'post_edit_form': post_edit_form,
                                                   'post_id': post_id})


def user_registration(request):
    if request.method == 'POST':
        user_registration_form = UserRegistrationForm(request.POST)
        if user_registration_form.is_valid():
            user_registration_form.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        user_registration_form = UserRegistrationForm()
    return render(request, 'blog/user_registration.html', {
        'user_registration_form': user_registration_form
    })


def user_authentication(request):
    if request.method == 'POST':
        user_authentication_form = UserAuthenticationForm(request.POST)
        if user_authentication_form.is_valid():
            if User.objects.filter(
                    username=user_authentication_form.cleaned_data['username']
            ):
                username = user_authentication_form.cleaned_data['username']
                return HttpResponseRedirect(
                    reverse('blog:user_profile', args=[username])
                )
    else:
        user_authentication_form = UserAuthenticationForm()
    return render(
        request,
        'blog/user_authentication.html',
        {'user_authentication_form': user_authentication_form}
    )


def user_profile(request, username):

    return render(request, 'blog/user_profile.html', {'username': username})
