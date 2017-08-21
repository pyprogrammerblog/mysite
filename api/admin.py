from django.contrib import admin
from django.contrib import messages
from .models import APIKey
from .helpers import generate_key


class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'modified')

    fieldsets = (
        ('Required Information', {'fields': ('name',)}),
        ('Additional Information', {'fields': ('key_message',)}),
    )
    readonly_fields = ('key_message',)

    search_fields = ('id', 'name',)

    def has_delete_permission(self, request, obj=None):
        return False

    def key_message(self, obj):
        if obj.key:
            return "Hidden"
        return "The API Key will be generated once you click save."

    def save_model(self, request, obj, form, change):
        APIKey.objects.all().delete()
        if not obj.key:
            obj.key = generate_key()
            messages.add_message(request,
                                 messages.WARNING, ('The API Key for {0} is {1}. Please note it since you will not be '
                                                    'able to see it again.'.format(obj.name, obj.key)))
        obj.save()

admin.site.register(APIKey, ApiKeyAdmin)