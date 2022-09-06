from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'blog'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.index, name='index'),
    path('posts/add', views.post_add, name='post_add'),
    path('posts/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('posts/remove/<int:post_id>', views.post_remove, name='post_remove'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('category/<str:category>', views.posts_by_category, name='posts_by_category'),

    # path('users/registration', views.user_registration, name='user_registration'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='user_login'),
    # path('users/login', views.user_login, name='user_login'),
    # path('users/logout', views.user_logout, name='user_logout'),
    # path('users/profile/<str:username>', views.user_profile, name='user_profile')
]
