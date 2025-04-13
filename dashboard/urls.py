from django.urls import path
from . views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    # path for category
    path('categories/', categories, name='categories'),
    path('categories/add/', add_categories, name='add_categories'),
    path('categories/edit/<int:pk>/', edit_categories, name='edit_categories'),
    path('categories/delete/<int:pk>/', delete_categories, name='delete_categories'),
    # path for post
    path('posts/', posts, name='posts'),
    path('posts/add', add_posts, name='add_posts'),
    path('posts/edit/<int:pk>/', edit_posts, name='edit_posts'),
    path('posts/delete/<int:pk>/', delete_posts, name='delete_posts'),
    # path for users
    path('users/', users, name='users'),
    path('users/add', add_users, name='add_users'),
    path('users/edit/<int:pk>', edit_users, name='edit_users'),
    path('users/<int:pk>/password/', change_user_password, name='password'),
    path('users/delete/<int:pk>', delete_users, name='delete_users'),
]
