from import_export import resources
from .models import BlogEntry, Contact, Tag, Image


class BlogEntryResource(resources.ModelResource):

    class Meta:
        model = BlogEntry


class ContactResource(resources.ModelResource):

    class Meta:
        model = Contact


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag


class ImageResource(resources.ModelResource):
    class Meta:
        model = Image
