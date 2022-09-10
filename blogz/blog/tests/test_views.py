from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ..models import Post
from ..forms import CommentForm

import datetime


def create_post(title, category=1, days_offset=0, author='john_doe'):
    """
    Creates a post with a given title and number of days offset to now.
    """
    content = "Test post content."
    publication_date = timezone.now() + datetime.timedelta(days=days_offset)
    email = author + '@example.com'
    owner = User.objects.create(username=author, email=email)
    return Post.objects.create(
        title=title,
        content=content,
        publication_date=publication_date,
        owner_id=owner.id,
        category=category
    )


def create_user(username='john_doe', first_name='John', last_name='Doe', email='john_doe@example.com'):
    """
    Creates a user with a given username.
    """
    return User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )


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
        self.assertQuerysetEqual(response.context['object_list'], [post_from_category_1])


class PostDetailViewTests(TestCase):
    def setUp(self):
        create_post("New post")

    def test_post(self):
        """
        Post is displayed.
        """
        post = Post.objects.get(title="New post")
        url = reverse('blog:post_detail', args=[post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)
