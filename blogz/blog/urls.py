from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/add', views.post_add, name='post_add'),
    path('posts/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('posts/<slug:slug>', views.post_detail, name='post_detail'),
    path('category/<str:category>', views.posts_by_category, name='posts_by_category'),
    path('users/registration', views.user_registration, name='user_registration'),
    path('users/authentication', views.user_authentication, name='user_authentication'),
    path('users/profile/<str:username>', views.user_profile, name='user_profile')
]
