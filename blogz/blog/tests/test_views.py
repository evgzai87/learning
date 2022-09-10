from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ..models import Post
from ..forms import CommentForm

import datetime


class IndexViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="New post", content="Post content", category=1, owner_id=user.id)

    def test_post(self):
        """
        Post is displayed.
        """
        post_list = Post.objects.all()
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertQuerysetEqual(response.context['object_list'], post_list)


class PostsByCategoryViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="Post from category 1", content="Post content", category=1, owner_id=user.id)
        Post.objects.create(title="Post from category 2", content="Post content", category=2, owner_id=user.id)

    def test_two_posts_in_different_categories(self):
        """
        Only one post is displayed for a given category.
        """
        post_from_category_1 = Post.objects.get(title="Post from category 1")
        url = reverse('blog:posts_by_category', args=['1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertQuerysetEqual(response.context['object_list'], [post_from_category_1])


class PostDetailViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="New post", content="Post content", category=1, owner_id=user.id)

    def test_basic(self):
        """
        . response.status_code is 200
        . blog/post_detail.html template is used to render page
        """
        post = Post.objects.get(title="New post")
        url = reverse('blog:post_detail', args=[post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['post'], post)


class PostCreateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="New post", content="Post content", category=1, owner_id=user.id)

    def test_basic(self):
        """
        . response.status_code is 200
        . blog/post_form.html template is used to render page
        """
        url = reverse('blog:post_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostUpdateViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="New post", content="Post content", category=1, owner_id=user.id)

    def test_basic(self):
        """
        . response.status_code is 200
        . blog/post_form.html template is used to render page
        """
        post = Post.objects.get(title='New post')
        url = reverse('blog:post_edit', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostDeleteViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_doe')
        Post.objects.create(title="New post", content="Post content", category=1, owner_id=user.id)

    def test_basic(self):
        """
        . response.status_code is 200
        . blog/post_form.html template is used to render page
        """
        post = Post.objects.get(title='New post')
        url = reverse('blog:post_remove', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'blog/post_form.html')


class UserRegistrationViewTests(TestCase):
    def setUp(self):
        User.objects.create(username='john_doe')

    def test_basic(self):
        """
        . response.status_code is 200
        . registration/registration.html template is used to render page
        """
        url = reverse('blog:registration')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')


class ProfileViewTests(TestCase):
    def setUp(self):
        User.objects.create(username='john_doe')

    def test_basic(self):
        """
        . response.status_code is 200
        . registration/profile.html template is used to render page
        """
        url = reverse('blog:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')


