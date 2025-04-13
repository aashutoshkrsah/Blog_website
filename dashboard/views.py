from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import *
from .forms import CategoryForm, AddPostForm, AddUserForm, SetPasswordForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from utils.permissions import is_reader, is_manager, is_superuser

# Create your views here.

# dashboard view

@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
    # Check if the user belongs to the "Reader" group using the utility function
    if is_reader(request.user):
        # If user is in the Reader group, show a permission error and redirect
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')  # Redirect to a safe page like the homepage or login
    
    # Fetch the counts of blogs and categories for the dashboard
    blogs_count = Blogs.objects.all().count()
    categories_count = Category.objects.all().count()
    
    # Pass the data to the template (context dictionary)
    context = {'blogs_count': blogs_count, 'categories_count': categories_count}
    
    # Render the dashboard template with the context
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    # Check if the user belongs to the "Reader" group
    if is_reader(request.user):
        # If user is in the Reader group, show a permission error and redirect
        messages.error(request, "You do not have permission to access categories.")
        return redirect('home')  # Redirect to a safe page like the homepage or login

    # If the user is not a Reader, render the categories page
    return render(request, 'dashboard/categories.html')

def add_categories(request):
    # Check if the user is in the "Reader" group
    if is_reader(request.user):
        # If the user is in the Reader group, deny access and show a message
        messages.error(request, "You do not have permission to add categories.")
        return redirect('home')  # Redirect to a safe page like the homepage or login

    # Handle the POST request to add a new category
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new category
            messages.success(request, 'Category has been created successfully!')
            return redirect('categories')  # Redirect to the categories page after successful creation

    # If the request is GET, render the add category form
    form = CategoryForm()
    context = {'form': form}
    return render(request, 'dashboard/add_categories.html', context)
            
        


def edit_categories(request, pk):
    # Fetch the category to be edited
    category = get_object_or_404(Category, pk=pk)
    
    # Check if the user is in the "Reader" group
    if is_reader(request.user):
        # If the user is in the Reader group, deny access and show a message
        messages.error(request, "You do not have permission to edit categories.")
        return redirect('categories')  # Redirect to the categories page or a safe page
    
    # If the user is not in the Reader group, allow editing
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()  # Save the updated category
            messages.success(request, 'Category has been updated successfully!')
            return redirect('categories')  # Redirect to the categories page after successful update
    
    # If the request is GET, render the edit category form
    form = CategoryForm(instance=category)
    context = {'form': form}
    return render(request, 'dashboard/edit_categories.html', context)


def delete_categories(request, pk):
    # Fetch the category to be deleted
    category = get_object_or_404(Category, pk=pk)
    
    # Check if the user is in the "Manager" or "Superuser" group
    if not (is_manager(request.user) or is_superuser(request.user)):
        # If the user is not a Manager or Superuser, deny access and show a message
        messages.error(request, "You do not have permission to delete this category.")
        return redirect('categories')  # Redirect to the categories page
    
    # If the user is authorized (Manager or Superuser), delete the category
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('categories')  # Redirect to the categories page after successful deletion

def posts(request):
    # Check if the user is allowed to view the posts
    if is_reader(request.user):
        # If the user is a Reader, show an error message and redirect them
        messages.error(request, "You do not have permission to view posts.")
        return redirect('home')  # Redirect to a different page (home or another)

    # Fetch all the posts if the user is allowed to view them
    posts = Blogs.objects.all()

    # If the user is authorized, render the posts page
    context = {'posts': posts}
    return render(request, 'dashboard/posts.html', context)

@login_required(login_url=reverse_lazy('login'))  # Ensure the user is logged in
def add_posts(request):
    # Check if the user is allowed to add posts (Editors, Managers, Superusers)
    if is_reader(request.user):
        # If the user is a Reader, show an error message and redirect them
        messages.error(request, "You do not have permission to add posts.")
        return redirect('home')  # Redirect to a page where the user has access

    # If it's a POST request, handle form submission
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Associate the post with the logged-in user
            post.save()  # Save the post to the database

            # Optionally set the slug after saving the post
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()

            messages.success(request, 'Post has been created successfully!')
            return redirect('posts')  # Redirect to the posts list page after successful submission
        else:
            print(form.errors)  # Print form errors if the form is not valid (for debugging)
    
    form = AddPostForm()  # Initialize the form if it's a GET request or the form is invalid
    context = {'form': form}  # Pass the form to the template
    return render(request, 'dashboard/add_posts.html', context)  # Render the template with the form

@login_required(login_url=reverse_lazy('login'))  # Ensure the user is logged in
def edit_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    
    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        # If the user is not the author, display an error message
        messages.error(request, "You are not authorized to edit this post.")
        return redirect('posts')  # Redirect to the list of posts if unauthorized
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)  # Populate form with post data
        if form.is_valid():
            updated_post = form.save(commit=False)
            # Ensure the post author is not changed (preserve the original author)
            updated_post.author = post.author  # Keep the original author
            updated_post.save()
            
            # Generate and save the slug based on the title
            title = form.cleaned_data['title']
            updated_post.slug = slugify(title)
            updated_post.save()
            
            messages.success(request, 'Post has been updated successfully!')
            return redirect('posts')  # Redirect to the posts list after saving
    
    else:
        form = AddPostForm(instance=post)  # Initialize form with the current post data
    
    context = {'form': form}  # Pass the form to the template
    return render(request, 'dashboard/edit_posts.html', context)  # Render the template with the form

@login_required(login_url=reverse_lazy('login'))  # Ensure the user is logged in
def delete_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)

    # Check if the logged-in user is the author of the post or has Manager/Superuser permissions
    if post.author != request.user and not (is_manager(request.user) or is_superuser(request.user)):
        # If the user is not the author, manager, or superuser, show an error message
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('posts')  # Redirect to the list of posts if unauthorized

    # Delete the post if authorized
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('posts')  # Redirect to the posts list after deletion

@login_required(login_url=reverse_lazy('login'))  # Ensure the user is logged in
def users(request):
    # Prevent Readers from accessing
    if is_reader(request.user):
        messages.error(request, "You are not authorized to view users.")
        return redirect('dashboard')

    # Allow only Manager and Superuser to access
    if not (is_manager(request.user) or is_superuser(request.user)):
        messages.error(request, "Only Managers and Superusers can view users.")
        return redirect('dashboard')

    users = User.objects.all()
    context = {'users': users}
    return render(request, 'dashboard/users.html', context)

@login_required(login_url=reverse_lazy('login'))
def add_users(request):
    # Block Readers entirely
    if is_reader(request.user):
        messages.error(request, "You are not authorized to add users.")
        return redirect('dashboard')

    # Allow only Manager and Superuser
    if not (is_manager(request.user) or is_superuser(request.user)):
        messages.error(request, "Only Managers and Superusers can add users.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New User Added Successfully!')
            return redirect('users')

    form = AddUserForm()
    context = {'form': form}
    return render(request, 'dashboard/add_users.html', context)


@login_required(login_url=reverse_lazy('login'))
def edit_users(request, pk):
    # Readers cannot access this page
    if is_reader(request.user):
        messages.error(request, "You are not authorized to edit users.")
        return redirect('dashboard')

    # Only Manager or Superuser can edit users
    if not (is_manager(request.user) or is_superuser(request.user)):
        messages.error(request, "Only Managers and Superusers can edit users.")
        return redirect('dashboard')

    user = get_object_or_404(User, pk=pk)  # Get the user by primary key

    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Updated Successfully!')
            return redirect('users')
    else:
        form = AddUserForm(instance=user)

    context = {'form': form}
    return render(request, 'dashboard/edit_users.html', context)


@login_required(login_url=reverse_lazy('login'))
def change_user_password(request, pk):
    """
    Only Superuser and Manager can update another user's password.
    """
    # Check if the user is allowed
    if not (is_superuser(request.user) or is_manager(request.user)):
        messages.error(request, "You are not authorized to change user passwords.")
        return redirect('dashboard')  # or wherever your main dashboard is

    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password updated successfully.")
            return redirect('users')  # Change this to your actual URL name
    else:
        form = SetPasswordForm(user)

    context = {'form': form, 'user': user}
    return render(request, 'dashboard/change_password.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_users(request, pk):
    """
    Allows only Superuser and Manager to delete users.
    """
    if not (is_superuser(request.user) or is_manager(request.user)):
        messages.error(request, "You are not authorized to delete users.")
        return redirect('users')

    user = User.objects.filter(pk=pk).first()
    if user:
        user.delete()
        messages.success(request, 'User deleted successfully!')
    else:
        messages.warning(request, 'User not found or already deleted.')

    return redirect('users')