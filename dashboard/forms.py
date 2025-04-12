from django import forms
from blogs.models import Category, Blogs
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('title', 'category', 'blog_image', 'short_description', 'blog_body', 'status',  'is_featured')
        
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')