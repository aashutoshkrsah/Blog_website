from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Blogs, Category
from django.db.models import Q


# Create your views here.

# fetch blogs according to the category
def posts_by_category(request, category_id):
    posts = Blogs.objects.filter(status='published', category= category_id)
    try:
        category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    context = {'posts':posts, 'category':category}
    return render(request, 'posts_by_category.html', context)

def blogs(request, slug):
    single_post = get_object_or_404(Blogs, slug=slug, status= 'published')
    context = {'single_post': single_post}
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blog = Blogs.objects.filter(Q(title__icontains =keyword) | Q(short_description__icontains =keyword) | Q(blog_body__icontains =keyword), status = 'published')
    context = {'blog':blog, 'keyword':keyword}
    return render(request, 'search.html', context)