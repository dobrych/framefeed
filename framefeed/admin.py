from django.contrib import admin
from framefeed.models import default_model, Meta
from framefeed.utils import django_is_lower_1_2


if not django_is_lower_1_2():
    class MetaInline(admin.TabularInline):
        model = default_model.meta.through
        extra = 1

class MetaFieldAdmin(admin.ModelAdmin):
    pass

class PhotoPostAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'tags', 'published', 'publish_at', 'updated_at')
    list_filter = ('published', 'publish_at')
    date_hierarchy = 'publish_at'
    exclude = ('meta',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    if not django_is_lower_1_2():
        inlines = (MetaInline,)

admin.site.register(default_model, PhotoPostAdmin)
admin.site.register(Meta, MetaFieldAdmin)