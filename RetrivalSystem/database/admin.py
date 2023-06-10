from django.contrib import admin

from .models import (
    Article, 

    Organization, 
    Category, 
    Region, 
    
    Tag, 
    PrimaryTags, 
    SecondaryTags, 
)

from import_export.admin import ImportExportModelAdmin

# Register your models here.


class ArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(Article, ArticleAdmin)


class OrganizationAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(Organization, OrganizationAdmin)

class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(Category, CategoryAdmin)

class RegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(Region, RegionAdmin)


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(Tag, TagAdmin)

class PrimaryTagsAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(PrimaryTags, PrimaryTagsAdmin)

class SecondaryTagsAdmin(ImportExportModelAdmin, admin.ModelAdmin):...
admin.site.register(SecondaryTags, SecondaryTagsAdmin)
