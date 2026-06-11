from django.contrib import admin

from .models import ForumCategory, ForumComment, ForumPost


admin.site.register(ForumCategory)
admin.site.register(ForumPost)
admin.site.register(ForumComment)
