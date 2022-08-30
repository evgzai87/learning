from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('post/add', views.post_add, name='post_add'),
    path('post/edit/<int:post_id>', views.post_edit, name='post_edit')
]
