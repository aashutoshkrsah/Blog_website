from django.shortcuts import render, redirect
from blogs.models import Category, Blogs
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.core.paginator import Paginator


def home(request):
    # Fetch all categories to display in the sidebar or navigation
    categories = Category.objects.all()

    # Fetch featured posts, ordered by most recent
    featured_post = Blogs.objects.filter(is_featured=True).order_by('-created_at')

    # Fetch non-featured (recent) published posts, ordered by most recent
    posts = Blogs.objects.filter(is_featured=False, status='published').order_by('-created_at')

    # Set up pagination: Display 2 posts per page
    paginator = Paginator(posts, 2)

    # Get the current page number from the URL query parameters
    page_number = request.GET.get('page')

    # Get the corresponding page of posts based on the page number
    post_final = paginator.get_page(page_number)

    # Prepare the context to pass to the template
    context = {
        'categories': categories,
        'featured_post': featured_post,
        'posts': posts,  # All posts (this will be the non-featured, paginated posts)
        'post_final': post_final,  # Paginated posts to be displayed on the home page
    }

    # Render the home template with the provided context
    return render(request, 'home.html', context)


# Register view handles the user registration process
def register(request):
    # Check if the request method is POST, meaning the form has been submitted
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Initialize form with the submitted data
        # Check if the form data is valid
        if form.is_valid():
            form.save()  # Save the user to the database
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()  # Initialize an empty form if it's a GET request
    
    # Pass the form to the context for rendering
    context = {'form': form}
    return render(request, 'register.html', context)  # Render the registration page with the form

# Login view handles the user login process
def login(request):
    # Check if the request method is POST, meaning the form has been submitted
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # Initialize form with submitted data
        # Check if the form data is valid
        if form.is_valid():
            username = form.cleaned_data['username']  # Get the username from the cleaned data
            password = form.cleaned_data['password']  # Get the password from the cleaned data
            
            # Authenticate the user using the provided username and password
            user = auth.authenticate(username=username, password=password)
            
            # If authentication is successful
            if user is not None:
                auth.login(request, user)  # Log the user in
                return redirect('dashboard')  # Redirect to the dashboard after successful login
    else:
        form = AuthenticationForm()  # Initialize an empty form if it's a GET request
    
    # Pass the form to the context for rendering
    context = {'form': form}
    return render(request, 'login.html', context)  # Render the login page with the form

# User logout view logs the user out and redirects to the login page
def user_logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page after logging out

# Edit post view renders the edit post page
def edit_post(request):
    return render(request, 'editPost.html')  # Render the page where users can edit a post
