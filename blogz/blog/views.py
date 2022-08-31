from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post
from .forms import PostAddForm, PostEditForm


def index(request):
    now = timezone.now()
    posts_list = Post.objects.filter(publication_date__lte=now).order_by('-publication_date')
    context = {'posts_list': posts_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
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
