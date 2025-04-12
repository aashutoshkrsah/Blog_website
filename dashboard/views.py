from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import *
from .forms import CategoryForm, AddPostForm, AddUserForm
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def dashboard(request):
    blogs_count = Blogs.objects.all().count()
    categories_count = Category.objects.all().count()
    context = {'blogs_count':blogs_count, 'categories_count':categories_count}
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html')

def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been created successfully!')
            return redirect('categories')
            
        
    form = CategoryForm()
    context = {'form':form}
    return render(request, 'dashboard/add_categories.html', context)

def edit_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been updated successfully!')
            return redirect('categories')  
    form = CategoryForm(instance=category)
    context = {'form':form}
    return render(request, 'dashboard/edit_categories.html', context)

def delete_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('categories')

def posts(request):
    posts = Blogs.objects.all()
    context = {'posts':posts}
    return render(request, 'dashboard/posts.html', context)

def add_posts(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post has been created successfully!')
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()           
            return redirect('posts')
        else:
            print(form.errors)
    form = AddPostForm()
    context = {'form': form}
    return render(request, 'dashboard/add_posts.html', context)

def edit_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user 
            updated_post.save()
            messages.success(request, 'Post has been updated successfully!')
            title = form.cleaned_data['title']
            updated_post.slug = slugify(title)
            updated_post.save()
            
            return redirect('posts')
    else:
        form = AddPostForm(instance=post)
    
    context = {'form': form}
    return render(request, 'dashboard/edit_posts.html', context)

def delete_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('posts')

def users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'dashboard/users.html', context)

def add_users(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New User Added Successfully !')
            return redirect('users')
    form = AddUserForm()
    context = {'form':form}
    return render(request, 'dashboard/add_users.html', context)

def edit_users(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Updated Successfully!')
            return render('users')
    form =AddUserForm(instance=user)
    context = {'form':form}
    return render(request, 'dashboard/edit_users.html', context)

def delete_users(request, pk):
    user = User.objects.filter(pk=pk).first()
    if user:
        user.delete()
        messages.success(request, 'User deleted successfully!')
    else:
        messages.warning(request, 'User not found or already deleted.')
    return redirect('users')