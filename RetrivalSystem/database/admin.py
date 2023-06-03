from django.contrib import admin

from .models import (
    Categories, 
    Article, 
)

# Register your models here.

admin.site.register(Categories)
admin.site.register(Article)
