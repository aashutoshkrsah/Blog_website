
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from blogs.views import blogs, search


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/', include('blogs.urls')),
    path('blog/<slug:slug>/', blogs, name='blogs'),
    path('blogs/search/', search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', include('dashboard.urls')),
    # path('create_post/', views.create_post, name='create_blog'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

