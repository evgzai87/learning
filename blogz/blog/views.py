from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post, Category
from .forms import PostAddForm, PostEditForm, CategoryAddEditForm, UserRegistrationForm


def index(request):
    now = timezone.now()
    posts_list = Post.objects.filter(publication_date__lte=now).order_by('-publication_date')
    category_list = Category.objects.order_by('name')
    context = {
        'posts_list': posts_list,
        'category_list': category_list
    }
    return render(request, 'blog/index.html', context)


def posts_by_category(request, category_id):
    posts_list = Post.objects.filter(category=category_id
                                            ).order_by('-publication_date')
    context = {
        'posts_list': posts_list,
        'category_name': category_id
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


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


def categories(request):
    categories_list = Category.objects.all().order_by('name')
    print(f'---------CATEGORIES: {categories_list}')
    context = {'categories_list': categories_list}
    return render(request, 'blog/categories.html', context)


def category_add(request):
    if request.method == 'POST':
        category_add_form = CategoryAddEditForm(request.POST)
        if category_add_form.is_valid():
            category_add_form.save()
            return HttpResponseRedirect(reverse('blog:categories'))
    else:
        category_add_form = CategoryAddEditForm()
    return render(request, 'blog/category_add.html', {
        'category_add_form': category_add_form
    })


def category_edit(request, category_id):
    editing_category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_edit_form = CategoryAddEditForm(request.POST)
        if category_edit_form.is_valid():
            editing_category.name = request.POST['name']
            editing_category.save()
            return HttpResponseRedirect(reverse('blog:categories'))
    else:
        category_edit_form = CategoryAddEditForm(instance=editing_category)
    return render(request, 'blog/category_edit.html', {
        'category_edit_form': category_edit_form,
        'category_id': category_id
    })
