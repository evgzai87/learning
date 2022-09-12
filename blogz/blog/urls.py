from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import (
    IndexView,
    PostView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostsByCategoryView,
    ProfileView
)
from . import views


app_name = 'blog'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('', IndexView.as_view(), name='index'),
    path('posts/add', login_required(PostCreateView.as_view()), name='post_add'),
    path('posts/edit/<int:pk>', login_required(PostUpdateView.as_view()), name='post_edit'),
    path('posts/remove/<int:pk>', login_required(PostDeleteView.as_view()), name='post_remove'),
    path('posts/<int:pk>', PostView.as_view(), name='post_detail'),

    path('category/<int:category_id>', PostsByCategoryView.as_view(), name='posts_by_category'),

    path('accounts/registration', views.user_registration, name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('accounts/password_change/', login_required(auth_views.LoginView.as_view()), name='password_change'),
    # path('accounts/password_reset/', auth_views.LoginView.as_view(), name='password_change'),
]
