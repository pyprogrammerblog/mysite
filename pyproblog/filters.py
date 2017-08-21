import django_filters
from .models import BlogEntry


class BlogEntryFilter(django_filters.FilterSet):
    class Meta:
        model = BlogEntry
        fields = ['title', ]
