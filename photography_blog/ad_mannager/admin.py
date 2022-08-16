from django.contrib import admin

from .models import Category, Post, Profile, Status
from django_summernote.admin import SummernoteModelAdmin

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Post, BlogAdmin)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Profile)