from django.contrib import admin

from .models import Badge, PointEvent, UserProfile


admin.site.register(Badge)
admin.site.register(UserProfile)
admin.site.register(PointEvent)
