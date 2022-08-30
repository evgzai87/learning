from django.test import TestCase
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Post


def create_post(title, days_offset):
    """
    Creates a post with a given title and number of days offset to now.
    """
    content = "Test post content."
    publication_date = timezone.now() + datetime.timedelta(days=days_offset)
    return Post.objects.create(title=title, content=content, publication_date=publication_date)


class IndexViewTests(TestCase):
    def test_no_posts(self):
        """
        Appropriate message is displayed, if no posts exist.
        """
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are published yet.")
        self.assertQuerysetEqual(response.context['posts_list'], [])

    def test_future_post(self):
        """
        Post with publication date in the future is not displayed.
        """
        create_post(title='Future post', days_offset=2)
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertContains(response, "No posts are published yet.")
        self.assertQuerysetEqual(response.context['posts_list'], [])

    def test_past_post(self):
        """
        Post with publication date in the past is displayed.
        """
        past_post = create_post(title='Past post', days_offset=-3)
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['posts_list'], [past_post])

    def test_future_and_past_posts(self):
        """
        Only post with publication date in the past is displayed.
        """
        past_post = create_post(title='Past post', days_offset=-1)
        create_post(title='Future post', days_offset=12)
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['posts_list'], [past_post])

    def test_two_past_posts(self):
        """
        Two posts with publication date in the past are displayed.
        """
        past_post_1 = create_post(title='Past post', days_offset=-1)
        past_post_2 = create_post(title='Past post', days_offset=-14)
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['posts_list'], [past_post_1, past_post_2])
