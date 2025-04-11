from django.shortcuts import render, redirect
from blogs.models import Category, Blogs
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_featured=True).order_by('-created_at')
    posts = Blogs.objects.filter(is_featured=False, status='published').order_by('-created_at')[:2]
    context = {'categories': categories, 'featured_post':featured_post, 'posts':posts}
    return render(request, 'home.html', context)

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form = RegistrationForm()
        
    context = {'form':form}
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = auth.authenticate(username = username, password = password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
        
    context = {'form':form}
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page (or wherever you want)

# def create_post(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         category = request.POST.get('category')
#         image = request.FILES.get('blog_image')
#         short_description = request.POST.get('shortDesc')
#         long_description = request.POST.get('longDesc')
        
#         blog = Blogs.objects.create(
#             title=title,
#             category=category,
#             author=request.user,
#             blog_image=image,
#             short_description=short_description,
#             blog_body=long_description,
#             status='published',
#             is_featured=False
#         )
    
    
        
    return render(request, 'create_post.html')

def edit_post(request):
    return render(request, 'editPost.html')