from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('post/add', views.post_add, name='post_add'),
    path('post/edit/<int:post_id>', views.post_edit, name='post_edit'),
    path('categories', views.categories, name='categories'),
    path('category/add', views.category_add, name='category_add'),
    path('category/edit/<int:category_id>', views.category_edit, name='category_edit'),
    path('user/registration', views.user_registration, name='user_registration')
]
