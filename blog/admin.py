from django.contrib import admin
from .models import Post ,User,Profile, Category ,Tag ,Comment
from import_export.admin import ImportExportMixin

class ChoiceInline(admin.TabularInline):
    model = Post
    extra = 3


class PostAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['status','category','published_date','created_date','title','author']
    list_filter = ['status','category','published_date','created_date','title','author']
    list_display = ('status','category','published_date','created_date','title','author')

class UserAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['mobile','email']
    list_filter = ['mobile','email']
    list_display = ('mobile','email')


class CommentAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['post','name','email','created','updated','active','parent']
    list_filter = ['post','name','email','created','updated','active','parent']
    list_display = ('post','name','email','created','updated','active','parent')

class CategoryAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['title']
    list_display = ('title',)

class ProfileAdmin(ImportExportMixin,admin.ModelAdmin):
    search_fields = ['user']
    list_filter = ['user']
    list_display = ('user',)


admin.site.register(Post,PostAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)
