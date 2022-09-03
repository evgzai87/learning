from django.forms import ModelForm
from .models import Article, Category, User


class UserRegistrationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PostAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['content'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = Article
        fields = ['title', 'content', 'category_1', 'category_2', 'owner']
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
    class Meta:
        model = Article
        fields = ['title', 'content', 'category_1', 'owner']


class CategoryAddEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control'}
        )

    class Meta:
        model = Category
        fields = ['name']
