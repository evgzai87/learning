from django.test import TestCase
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
import datetime
from .models import Post, User


def create_post(
        title,
        days_offset,
        author='Author_1',
        email='author_1@example.com'
):
    """
    Creates a post with a given title and number of days offset to now.
    """

    content = "Test post content."
    publication_date = timezone.now() + datetime.timedelta(days=days_offset)
    owner = User.objects.create(username=author, email=email)
    return Post.objects.create(
        title=title,
        content=content,
        publication_date=publication_date,
        owner_id=owner.id
    )


def create_user(
        username='john_doe',
        first_name='John',
        last_name='Doe',
        email='john_doe@example.com'):
    """
    Creates a user with a given username.
    """
    return User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )


class ModelUserTests(TestCase):
    """
    . The __str__ method returns username
    """
    # def test_create_new_user(self):
    #     """
    #     User is saved to the DB.
    #     """
    #     created_user = create_user()
    #     users_from_db = User.objects.all()
    #     self.assertIn(created_user, users_from_db)
    #
    # def test_create_new_user_without_username(self):
    #     """
    #     A user without username is not saved in the DB.
    #     """
    #     # user created with empty string. Is it equal to not filled field?
    #     created_user = create_user(username='')
    #     users_from_db = User.objects.all()
    #     self.assertNotIn(created_user, users_from_db)
    #
    # def test_create_new_user_without_first_name(self):
    #     """
    #     A user without first_name is saved in the DB.
    #     """
    #     created_user = create_user(first_name='')
    #     users_from_db = User.objects.all()
    #     self.assertIn(created_user, users_from_db)
    #
    # def test_create_new_user_without_last_name(self):
    #     """
    #     A user without last_name is saved in the DB.
    #     """
    #     created_user = create_user(last_name='')
    #     users_from_db = User.objects.all()
    #     self.assertIn(created_user, users_from_db)
    #
    # def test_create_new_user_without_email(self):
    #     """
    #     A user without email is not saved in the DB.
    #     """
    #     created_user = create_user(email='')
    #     users_from_db = User.objects.all()
    #     self.assertNotIn(created_user, users_from_db)
    #
    # def test_create_user_with_not_unique_username(self):
    #     """
    #     User with not unique username is not saved in the DB.
    #     """
    #     created_first_user = create_user()
    #     created_user_with_not_unique_username = create_user(
    #         username='john_doe',
    #         first_name='John_2',
    #         last_name='Doe_2',
    #         email='john_doe_2@example.com'
    #     )
    #     users_from_db = User.objects.all()
    #     self.assertEquals(
    #         created_first_user.username,
    #         created_user_with_not_unique_username.username
    #     )
    #     self.assertNotIn(
    #         created_user_with_not_unique_username,
    #         users_from_db
    #     )
    #     self.assertIn(created_first_user, users_from_db)
    #
    # def test_create_user_with_not_unique_first_name(self):
    #     """
    #     User with not unique first_name is saved in the DB.
    #     """
    #     created_first_user = create_user()
    #     created_user_with_not_unique_first_name = create_user(
    #         username='john_doe_2',
    #         first_name='John',
    #         last_name='Doe_2',
    #         email='john_doe_2@example.com'
    #     )
    #     users_from_db = User.objects.all()
    #     self.assertEquals(
    #         created_first_user.first_name,
    #         created_user_with_not_unique_first_name.first_name
    #     )
    #     self.assertIn(
    #         created_user_with_not_unique_first_name,
    #         users_from_db
    #     )
    #     self.assertIn(created_first_user, users_from_db)
    #
    # def test_create_user_with_not_unique_last_name(self):
    #     """
    #     User with not unique last_name is saved in the DB.
    #     """
    #     created_first_user = create_user()
    #     created_user_with_not_unique_last_name = create_user(
    #         username='john_doe_2',
    #         first_name='John_2',
    #         last_name='Doe',
    #         email='john_doe_2@example.com'
    #     )
    #     users_from_db = User.objects.all()
    #     self.assertEquals(
    #         created_first_user.last_name,
    #         created_user_with_not_unique_last_name.last_name
    #     )
    #     self.assertIn(
    #         created_user_with_not_unique_last_name,
    #         users_from_db
    #     )
    #     self.assertIn(created_first_user, users_from_db)
    #
    # # def test_create_user_with_not_unique_email(self):
    # #     """
    # #     User with not unique username is not saved in the DB.
    # #     """
    # #     created_first_user = create_user()
    # #     created_user_with_not_unique_email = create_user(
    # #         username='john_doe_2',
    # #         first_name='John_2',
    # #         last_name='Doe_2',
    # #         email='john_doe@example.com'
    # #     )
    # #     users_from_db = User.objects.all()
    # #     self.assertEquals(
    # #         created_first_user.email,
    # #         created_user_with_not_unique_email.email
    # #     )
    # #     self.assertNotIn(
    # #         created_user_with_not_unique_email,
    # #         users_from_db
    # #     )
    # #     self.assertIn(created_first_user, users_from_db)

    def test_str_method(self):
        """
        User with not unique username is not saved in the DB.
        """
        created_first_user = create_user()
        user_from_db = User.objects.get(id=1)
        self.assertEquals(user_from_db.__str__(), 'john_doe')


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
        past_post = create_post(
            title='Past post',
            author='Author_1',
            email='author_1@example.com',
            days_offset=-1
        )
        create_post(
            title='Future post',
            author='Author_2',
            email='author_2@example.com',
            days_offset=12
        )
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['posts_list'], [past_post])

    def test_two_past_posts(self):
        """
        Two posts with publication date in the past are displayed.
        """
        past_post_1 = create_post(
            title='Past post',
            author='Author_1',
            email='author_1@example.com',
            days_offset=-1
        )
        past_post_2 = create_post(
            title='Past post',
            author='Author_2',
            email='author_2@example.com',
            days_offset=-14
        )
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['posts_list'], [past_post_1, past_post_2])
