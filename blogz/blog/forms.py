from django.forms import ModelForm
from .models import Post, Comment


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control'}
            )

    class Meta:
        model = Comment
        fields = ['content', 'owner', 'post']


class PostAddForm(ModelForm):
    # Add bootstrap classes for the form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'owner']
        help_texts = {
            'title': 'Укажите название статьи',
            'content': 'Напишите что-нибудь по теме'
        }


class PostEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']
