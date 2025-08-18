from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from .models import Post, Category, Comment, Like
from django.http import JsonResponse
from .forms import CommentForm, SearchForm
from django.contrib.auth import get_user_model

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
    post = get_object_or_404(Post, slug=slug, is_published=True)
    comments = Comment.objects.filter(post=post, parent=None, is_approved=True)
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(is_published=True).exclude(id=post.id)[:4]

    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        parent_id = request.POST.get('parent_id')

        parent = Comment.objects.get(id=parent_id) if parent_id else None

        Comment.objects.create(
            post=post,
            name=name,
            text=text,
            parent=parent
        )
        messages.success(request, 'Your comment was added!')
        return redirect(post.get_absolute_url())

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': SearchForm(),  # optional
    })

def like_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    ip = get_client_ip(request)

    like, created = Like.objects.get_or_create(post=post, ip_address=ip)
    return JsonResponse({
        'status': 'liked' if created else 'already_liked',
        'likes': post.likes.count()
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


def create_superuser_if_not_exists():
    User = get_user_model()
    if not User.objects.filter(username="drey").exists():
        User.objects.create_superuser("drey", "cobi658@gmail.com", "mikay2021")

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
