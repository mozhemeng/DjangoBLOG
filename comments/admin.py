from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'text', 'created_time','post']

admin.site.register(Comment, CommentAdmin)