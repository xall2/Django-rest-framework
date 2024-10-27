from django.contrib import admin
from .models import Post
# Register your models here.


class PostsAdmin(admin.ModelAdmin):
    list_display = ('title','content','created_at')


admin.site.register(Post,PostsAdmin)