from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Post, User

from django.contrib.auth import \
    authenticate, \
    login, \
    logout
from django.shortcuts import \
    render, \
    reverse, \
    get_object_or_404
from .forms import PostAddForm, PostEditForm


def index(request):
    now = timezone.now()
    posts_list = Post.objects.filter(publication_date__lte=now)
    context = {
        'posts_list': posts_list
    }
    return render(
        request,
        'blog/index.html',
        context)


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


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post
    }
    return render(
        request,
        'blog/post_detail.html',
        context
    )


@login_required(login_url='/users/login')
def post_add(request):
    if request.method == 'POST':
        post_add_form = PostAddForm(request.POST, request.FILES)
        if post_add_form.is_valid():
            user = post_add_form.cleaned_data['owner']
            post_add_form.save()
            return HttpResponseRedirect(reverse('blog:user_profile', args=[user]))
    else:
        post_add_form = PostAddForm()
    return render(
        request,
        'blog/post_add.html',
        {'post_add_form': post_add_form}
    )


@login_required(login_url='/users/login')
def post_edit(request, post_id):
    editing_post = Post.objects.filter(pk=post_id)
    user = editing_post[0].owner
    if request.method == 'POST':
        post_edit_form = PostEditForm(
            request.POST,
            request.FILES,
            instance=editing_post[0]
        )

        if post_edit_form.is_valid():
            new_title = post_edit_form.cleaned_data['title']
            new_content = post_edit_form.cleaned_data['content']
            new_category = post_edit_form.cleaned_data['category']
            editing_post.update(title=new_title)
            editing_post.update(content=new_content)
            editing_post.update(category=new_category)

            return HttpResponseRedirect(reverse('blog:user_profile', args=[user]))
    else:
        post_edit_form = PostEditForm(instance=editing_post[0])

    return render(
        request,
        'blog/post_edit.html',
        {
            'post_edit_form': post_edit_form,
            'post_id': post_id
        }
    )


@login_required(login_url='/users/login')
def post_remove(request, post_id):
    owner = get_object_or_404(Post, id=post_id).owner
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('blog:user_profile', args=[owner]))


def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = UserCreationForm()
    return render(
        request,
        'registration/registration.html',
        {'form': form}
    )


# def user_login(request):
#     if request.method == 'POST':
#         user_login_form = UserLoginForm(request.POST)
#         if user_login_form.is_valid():
#             username = user_login_form.cleaned_data['username']
#             password = user_login_form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(
#                     reverse('blog:user_profile', args=[username])
#                 )
#             else:
#                 print(f'Login failed for user {user}')
#     else:
#         user_login_form = UserLoginForm()
#     return render(
#         request,
#         'blog/user_login.html',
#         {'user_authentication_form': user_login_form}
#     )


# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('blog:index'))


# @login_required(login_url='/users/login')
# def user_profile(request, username):
#     user_posts = User.objects.get(username=username).post_set.all()
#     return render(
#         request,
#         'blog/user_profile.html',
#         {
#             'username': username,
#             'user_posts': user_posts
#         }
#     )
