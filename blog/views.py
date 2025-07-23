from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import Post, Category, Comment
from .forms import CommentForm, SearchForm
# Create your views here.

def home(request):
    """Homepage view with paginated posts"""
    posts = Post.objects.filter(is_published=True).select_related('author', 'category')
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    # Get recent posts for sidebar
    recent_posts = Post.objects.filter(is_published=True)[:4]
    
    context = {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': SearchForm(),
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    """Individual post detail view"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = post.comments.filter(is_approved=True)
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True).exclude(id=post.id)[:4]
    
    # Handle comment form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': SearchForm(),
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Posts filtered by category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, is_published=True).select_related('author', 'category')
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    recent_posts = Post.objects.filter(is_published=True)[:4]
    
    context = {
        'posts': posts,
        'category': category,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': SearchForm(),
    }
    return render(request, 'blog/category_posts.html', context)


def search_posts(request):
    """Search posts by title and content"""
    form = SearchForm(request.GET)
    posts = Post.objects.none()
    query = None
    
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            posts = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(excerpt__icontains=query),
                is_published=True
            ).select_related('author', 'category')
    
    # Pagination
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True)[:4]
    
    context = {
        'posts': posts,
        'query': query,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': SearchForm(initial={'query': query}),
    }
    return render(request, 'blog/search_results.html', context)

from django.core.management import call_command
from django.http import HttpResponse

def run_migrations(request):
    call_command('migrate')
    return HttpResponse("Migrations complete.")


# def about(request):
#     """About page"""
#     categories = Category.objects.all()
#     recent_posts = Post.objects.filter(is_published=True)[:4]
    
#     context = {
#         'categories': categories,
#         'recent_posts': recent_posts,
#         'search_form': SearchForm(),
#     }
#     return render(request, 'blog/about.html', context)


# def contact(request):
#     """Contact page"""
#     categories = Category.objects.all()
#     recent_posts = Post.objects.filter(is_published=True)[:4]
    
#     context = {
#         'categories': categories,
#         'recent_posts': recent_posts,
#         'search_form': SearchForm(),
#     }
#     return render(request, 'blog/contact.html', context)