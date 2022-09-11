from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import CommentForm, PostAddForm
from ..models import Post


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', email='john_doe@example.com', password='paS$w0rd')
        self.post = Post.objects.create(title="New post", content="Post content", category=1, owner_id=self.user.pk)

        # --------------------------------------- PostAddForms
        self.post_form_filled = PostAddForm(
            data={
                'title': 'Some title',
                'content': 'Some content',
                'image': '',
                'category': 1,
                'owner': self.user.id
            }
        )
        self.post_form_without_title = PostAddForm(
            data={
                'title': '',
                'content': 'Some content',
                'image': '',
                'category': 1,
                'owner': self.user.id
            }
        )
        self.post_form_without_content = PostAddForm(
            data={
                'title': 'Some title',
                'content': '',
                'image': '',
                'category': 1,
                'owner': self.user.id
            }
        )
        self.post_form_without_category = PostAddForm(
            data={
                'title': 'Some title',
                'content': 'Some content',
                'image': '',
                'category': '',
                'owner': self.user.id
            }
        )
        self.post_form_without_owner = PostAddForm(
            data={
                'title': 'Some title',
                'content': 'Some content',
                'image': '',
                'category': '1',
                'owner': ''
            }
        )

        # --------------------------------------- CommentForm
        self.comment_form_filled = CommentForm(
            data={
                'content': 'Some content',
                'owner': self.user.id,
                'post': self.post.id
            }
        )
        self.comment_form_without_owner = CommentForm(
            data={
                'content': 'Some content',
                'owner': '',
                'post': self.post.id
            }
        )
        self.comment_form_without_post = CommentForm(
            data={
                'content': 'Some content',
                'owner': self.user.id,
                'post': ''
            }
        )


class CommentFormTests(BaseTest):
    def test_form_is_not_valid(self):
        """
        If any of content, owner and post field is empty, a form is not valid.
        """
        self.assertFalse(self.comment_form_without_owner.is_valid())
        self.assertFalse(self.comment_form_without_post.is_valid())

    def test_form_is_valid(self):
        """
        If all required fields are filled, a form is valid.
        """
        self.assertTrue(self.comment_form_filled.is_valid())


class PostAddFormTests(BaseTest):
    def test_form_is_not_valid(self):
        """
        If any of title, content, category and owner field is empty, a form is not valid.
        """
        self.assertFalse(self.post_form_without_title.is_valid())
        self.assertFalse(self.post_form_without_content.is_valid())
        self.assertFalse(self.post_form_without_category.is_valid())
        self.assertFalse(self.post_form_without_owner.is_valid())

    def test_form_is_valid(self):
        """
        If all required fields are filled, a form is valid.
        """
        self.assertTrue(self.post_form_filled.is_valid())
