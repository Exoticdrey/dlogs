from django.contrib import admin
from .models import Category, Post, Comment
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_post_count', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def get_post_count(self, obj):
        return obj.get_post_count()
    get_post_count.short_description = 'Posts Count'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'created_at']
    list_filter = ['category', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_published']
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'category', 'is_published')
        }),
        ('Content', {
            'fields': ('image', 'excerpt', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'get_short_text', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['name', 'email', 'text', 'post__title']
    readonly_fields = ['created_at']
    list_editable = ['is_approved']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'name', 'email', 'is_approved')
        }),
        ('Content', {
            'fields': ('text',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

    def get_short_text(self, obj):
        return obj.get_short_text()
    get_short_text.short_description = 'Comment Preview'