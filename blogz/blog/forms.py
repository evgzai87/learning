from django.forms import ModelForm
from .models import Post


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
        model = Post
        fields = ['title', 'content']


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']