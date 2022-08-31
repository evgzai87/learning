from django.test import TestCase
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Post, User


def create_post(title, days_offset):
    """
    Creates a post with a given title and number of days offset to now.
    """

    content = "Test post content."
    publication_date = timezone.now() + datetime.timedelta(days=days_offset)
    owner = User.objects.create(username='john_doe')
    # print(f'------------PUBL_DATE: {publication_date}')
    return Post.objects.create(
        title=title,
        content=content,
        publication_date=publication_date,
        owner_id=owner.id
    )


def create_user(username):
    """
    Creates a user with a given username.
    """
    first_name = 'John'
    last_name = 'Doe'
    email = 'john_doe@example.com'

    return User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )


class ModelUserTests(TestCase):
    """
    . Create new user with all fields filled in.
    .
    . Create new user whose username is not filled in.
    . Create new user whose first_name is not filled in.
    . Create new user whose last_name is not filled in.
    . Create new user whose email is not filled in.
    . Create new user whose registration_date is not filled in.
    .
    . Create two users with the same usernames.
    . Create two users with the same first_name.
    . Create two users with the same last_name.
    . Create two users with the same email.
    . Create two users with the same registration_date.
    .
    . Create user with registration_date in the future.
    . Create user with registration_date in the past.
    . The __str__ method returns username
    """
    def test_create_new_user(self):
        """
        User is saved to the DB.
        """
        created_user = create_user('john_doe')
        users_from_db = User.objects.get(id=1)
        # self.assertContains(users_from_db, created_user)
        # self.assertEqual(users_from_db[0], created_user)
        # not finished

    def test_create_new_user_without_username(self):
        """
        A user without username is not saved in the DB.
        """
        created_user = create_user('john_doe')
        saved_user = User.objects.get(id=1)
        # not finished


    def test_create_new_user_without_first_name(self):
        pass

    def test_create_new_user_without_last_name(self):
        pass

    def test_create_new_user_without_registration_date(self):
        pass


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
