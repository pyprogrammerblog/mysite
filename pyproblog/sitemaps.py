from django.contrib.sitemaps import Sitemap
from .models import BlogEntry


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return BlogEntry.publish.all()

    def lastmod(self, obj):
        return obj.published