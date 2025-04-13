from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Blogs, Category, Comment
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


# Create your views here.

# fetch blogs according to the category
def posts_by_category(request, category_id):
    try:
        # Try to get the category object by its primary key
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        # If category doesn't exist, redirect to home
        return redirect('home')

    # Fetch all published blog posts for the given category, ordered by most recent
    posts_list = Blogs.objects.filter(status='published', category=category_id).order_by('-created_at')

    # Set up pagination: Show 5 posts per page
    paginator = Paginator(posts_list, 3)

    # Get the current page number from the GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page of posts
    posts = paginator.get_page(page_number)

    # Prepare context to pass to the template
    context = {
        'posts': posts,
        'category': category
    }

    # Render the template with paginated posts and category info
    return render(request, 'posts_by_category.html', context)

# Blog detail view, displays a single blog post and handles comment submission
def blogs(request, slug):
    # Get the single blog post by its slug and ensure it is published
    single_post = get_object_or_404(Blogs, slug=slug, status='published')

    # Check if the request method is POST, meaning a comment is being submitted
    if request.method == 'POST':
        comment = Comment()  # Create a new Comment object
        comment.user = request.user  # Assign the current logged-in user as the commenter
        comment.blog = single_post  # Associate the comment with the specific blog post
        comment.comment = request.POST['comment']  # Get the comment text from the POST data
        comment.save()  # Save the comment to the database
        return HttpResponseRedirect(request.path_info)  # Redirect to the same page to show the new comment

    # Get all comments for the specific blog post
    comments = Comment.objects.filter(blog=single_post)
    # Count the number of comments for this blog post
    comments_counts = comments.count()

    # Pass the single post, comments, and comment count to the context for rendering
    context = {'single_post': single_post, 'comments': comments, 'comments_counts': comments_counts}
    return render(request, 'blogs.html', context)  # Render the blog detail page with the context

# Search view, handles searching for blog posts based on a keyword
def search(request):
    keyword = request.GET.get('keyword', '')

    # Filter and order results
    blog_list = Blogs.objects.filter(
        Q(title__icontains=keyword) |
        Q(short_description__icontains=keyword) |
        Q(blog_body__icontains=keyword),
        status='published'
    ).order_by('-created_at')  # Order by latest posts first

    # Paginate
    paginator = Paginator(blog_list, 3)
    page_number = request.GET.get('page')
    blog_page = paginator.get_page(page_number)

    context = {
        'blog': blog_page,
        'keyword': keyword
    }
    return render(request, 'search.html', context)
