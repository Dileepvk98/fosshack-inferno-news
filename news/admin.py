from django.contrib import admin

# Register your models here.
from .models import Post, Articles

admin.site.register(Post)
admin.site.register(Articles)