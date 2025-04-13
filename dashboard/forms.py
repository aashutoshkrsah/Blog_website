from django import forms
from blogs.models import Category, Blogs
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.urls import reverse
from django.utils.safestring import mark_safe

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
    
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('title', 'category', 'blog_image', 'short_description', 'blog_body', 'status',  'is_featured')
        
# UserCreationForm for creating users (includes password fields)
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    # Override the save method to handle many-to-many relationships
    def save(self, commit=True):
        user = super().save(commit=False)  # Get the user instance without saving
        if commit:
            user.save()  # Save the user instance
            self.save_m2m()  # Save many-to-many relationships (groups, permissions)
        return user
    
# Use UserChangeForm for editing user details
class AddUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email',
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only override password help text if editing an existing user
        if self.instance and self.instance.pk:
            change_password_url = reverse('password', kwargs={'pk': self.instance.pk})
            self.fields['password'].help_text = mark_safe(
                f"You can change the password using <a href='{change_password_url}'>this form</a>."
            )

    # Override the save method to handle many-to-many relationships
    def save(self, commit=True):
        user = super().save(commit=False)  # Get the user instance without saving
        if commit:
            user.save()  # Save the user instance
            self.save_m2m()  # Save many-to-many relationships (groups, permissions)
        return user
    
class AdminSetPasswordForm(SetPasswordForm):
    """
    A form that lets an admin set a new password for a user without requiring the old password.
    Inherits from Django's built-in SetPasswordForm.
    """
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']