from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    IndexView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostsByCategoryView
)
from . import views


app_name = 'blog'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('', IndexView.as_view(), name='index'),
    path('posts/add', PostCreateView.as_view(), name='post_add'),
    path('posts/edit/<int:pk>', PostUpdateView.as_view(), name='post_edit'),
    path('posts/remove/<int:pk>', PostDeleteView.as_view(), name='post_remove'),
    path('posts/<int:pk>', PostDetailView.as_view(), name='post_detail'),

    path('category/<int:category_id>', PostsByCategoryView.as_view(), name='posts_by_category'),

    path('accounts/registration', views.user_registration, name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/password_change/', auth_views.LoginView.as_view(), name='password_change'),
    # path('accounts/password_reset/', auth_views.LoginView.as_view(), name='password_change'),
]
