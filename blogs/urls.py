from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    
]