from django.contrib import admin

from .models import (
    Organization, 
    Category, 
    Article, 
    Region, 
)

# Register your models here.

admin.site.register(Organization)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Article)
