from django.test import TestCase
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from ..models import Post
from ..forms import CommentForm

import datetime


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', email='john_doe@example.com', password='paS$w0rd')
        self.post = Post.objects.create(title="New post", content="Post content", category=1, owner_id=self.user.pk)
        self.post_from_another_category = Post.objects.create(
            title="Post from category 1", content="Post content", category=2, owner_id=self.user.pk)
        self.non_existent_post_id = 99

        self.post_list = Post.objects.all()

        self.index_url = reverse('blog:index')
        self.posts_by_category_url = reverse('blog:posts_by_category', args=[self.post.category])
        self.post_detail_url = reverse('blog:post_detail', args=[self.post.pk])
        self.post_non_existent_detail_url = reverse('blog:post_detail', args=[self.non_existent_post_id])
        self.post_add_url = reverse('blog:post_add')
        self.post_edit_url = reverse('blog:post_edit', args=[self.post.pk])
        self.post_remove_url = reverse('blog:post_remove', args=[self.post.pk])
        self.registration_url = reverse('blog:registration')
        self.profile_url = reverse('blog:profile')

        return super().setUp()


class IndexViewTests(BaseTest):
    def test_can_view_page_correctly(self):
        """
        . response.status_code is 200
        . blog/index.html template is used to render page
        """
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')


class PostsByCategoryViewTests(BaseTest):
    def test_can_view_page_correctly(self):
        """
        . response.status_code is 200
        . blog/index.html template is used to render page
        """
        response = self.client.get(self.posts_by_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_two_posts_in_different_categories(self):
        """
        Only one post is displayed for a given category.
        """
        response = self.client.get(self.posts_by_category_url)
        self.assertQuerysetEqual(response.context['object_list'], [self.post])


class PostDetailViewTests(BaseTest):
    def test_can_view_page_correctly(self):
        """
        . response.status_code is 200
        . blog/post_detail.html template is used to render page
        """
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_non_existent_post(self):
        """
        When trying to display a non-existent post, a 404 error page is displayed.
        """
        response = self.client.get(self.post_non_existent_detail_url)
        self.assertEqual(response.status_code, 404)


class PostCreateViewTests(BaseTest):
    def test_anonymous_user_access(self):
        """
        Anonymous user is redirected to the login page.
        """
        response = self.client.get(self.post_add_url)
        self.assertRedirects(response, reverse('blog:login') + '?next=' + self.post_add_url)

    def test_authorized_user_access(self):
        """
        Authorized user can view this page.
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.get(self.post_add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostUpdateViewTests(BaseTest):
    def test_anonymous_user_access(self):
        """
        Anonymous user is redirected to the login page.
        """
        response = self.client.get(self.post_edit_url)
        self.assertRedirects(response, reverse('blog:login') + '?next=' + self.post_edit_url)

    def test_authorized_user_access(self):
        """
        Authorized user can view this page.
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.get(self.post_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostDeleteViewTests(BaseTest):
    def test_anonymous_user_access(self):
        """
        Anonymous user is redirected to the login page.
        """
        response = self.client.get(self.post_remove_url)
        self.assertRedirects(response, reverse('blog:login') + '?next=' + self.post_remove_url)

    def test_authorized_user_access(self):
        """
        Authorized user can view this page
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.get(self.post_remove_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')

    def test_redirect_on_success_deletion(self):
        """
        If post was deleted successful user is redirected to /accounts/profile url.
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.post(self.post_remove_url)
        self.assertRedirects(response, reverse('blog:profile'))

    def test_db_response_upon_deleted_post(self):
        """
        DB returns an empty Queryset upon request a deleted post.
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.post(self.post_remove_url)
        queryset_deleted_post = Post.objects.filter(pk=self.post.pk)
        self.assertQuerysetEqual(queryset_deleted_post, [])


class UserRegistrationViewTests(BaseTest):
    def test_can_view_page_correctly(self):
        """
        . response.status_code is 200
        . registration/registration.html template is used to render page
        """
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')


class ProfileViewTests(BaseTest):
    def test_anonymous_user_access(self):
        """
        Not authorized user can't view this page.
        anonymous user is redirected to login page.
        """
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, reverse('blog:login') + '?next=' + self.profile_url)

    def test_authorized_user_access(self):
        """
        Authorized user can view this page
        """
        self.client.login(username=self.user.username, password='paS$w0rd')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
