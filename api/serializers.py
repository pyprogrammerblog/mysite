from pyproblog.models import BlogEntry, Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tagname',)


class BlogEntrySerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = BlogEntry
        fields = ('title', 'subheading', 'tags', 'slug', 'body', 'published',)


class BlogEntryTitleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = BlogEntry
        fields = ('title', 'subheading', 'tags', 'slug', 'published',)
