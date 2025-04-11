from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import *
from .forms import CategoryForm

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
            return redirect('categories')  
    form = CategoryForm(instance=category)
    context = {'form':form}
    return render(request, 'dashboard/edit_categories.html', context)

def delete_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')