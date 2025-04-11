from django.urls import path
from . views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('categories/', categories, name='categories'),
    path('categories/add/', add_categories, name='add_categories'),
    path('categories/edit/<int:pk>/', edit_categories, name='edit_categories'),
    path('categories/delete/<int:pk>/', delete_categories, name='delete_categories'),
]
