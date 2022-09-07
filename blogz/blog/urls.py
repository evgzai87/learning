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

    path('accounts/registration', views.user_registration, name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/password_change/', auth_views.LoginView.as_view(), name='password_change'),
    # path('accounts/password_reset/', auth_views.LoginView.as_view(), name='password_change'),
]
