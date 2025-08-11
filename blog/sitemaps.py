from django.contrib.sitemaps import Sitemap
from .models import Post  # your blog model

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # or obj.date if you don’t have updated_at

    def location(self, obj):
        return f"/blog/{obj.slug}/"  # adjust if your blog URL is different
