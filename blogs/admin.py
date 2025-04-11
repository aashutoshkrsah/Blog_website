from django.contrib import admin
from .models import Category, Blogs

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at', 'updated_at')

admin.site.register(Category, CategoryAdmin)

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'blog_image', 'status', 'is_featured', 'created_at', 'updated_at')
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('id', 'title', 'category__category_name', 'status' )
    list_editable = ('is_featured', 'status',)  # list editable helps to edit the attributes of objects. there must be comma. if we don't give comma django won't take it as tuple
                    

admin.site.register(Blogs, BlogsAdmin)