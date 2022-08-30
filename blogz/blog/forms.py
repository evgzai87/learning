from django.forms import ModelForm
from .models import Post


class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']