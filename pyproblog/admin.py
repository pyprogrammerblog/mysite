from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import BlogEntry, Contact, Tag, Image, Subscriber, Email, EditableTemplate


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):

    list_display = ("tagname", "created",)
    list_filter = ('created', 'tagname',)
    search_fields = ('tagname',)


@admin.register(BlogEntry)
class BlogEntryAdmin(ImportExportModelAdmin):

    list_display = ('title', 'slug', 'subheading', 'author', 'published', 'status')
    list_filter = ('status', 'created', 'published', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('author', )
    date_hierarchy = 'published'
    ordering = ['status', 'published',]


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):

    list_display = ('name', 'email')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ['send_on', ]


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(ImportExportModelAdmin):

    list_display = ('email', 'created',)
    list_filter = ('email',)
    search_fields = ('email',)
    ordering = ['-created', ]
    fields = ['email', 'email_verified', ]


@admin.register(EditableTemplate)
class EditableTemplateAdmin(ImportExportModelAdmin):
    pass


@admin.register(Email)
class EmailRecordAdmin(ImportExportModelAdmin):
    pass
