from django.urls import path
from . import views
from .views import run_migrations  # or blog.views if not in same file


app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search'),
    path('run-migrations/', run_migrations),

    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]