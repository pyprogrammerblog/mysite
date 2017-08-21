from ..models import BlogEntry, Tag
from django.db.models import Count
from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag()
def total_posts():
    return BlogEntry.publish.count()


@register.simple_tag()
def latest_posts():
    return BlogEntry.publish.order_by('-published')[:3]


@register.simple_tag()
def categories():
    return Tag.objects.all()