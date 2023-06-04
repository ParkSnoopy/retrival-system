from django.contrib import admin

from .models import (
    Organization, 
    Category, 
    Article, 
)

# Register your models here.

admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(Article)
