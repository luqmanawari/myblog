from django.contrib import admin
from .models import Post, Comment, UserProfile

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'view_count', 'get_like_count', 'get_comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    inlines = [CommentInline]
    
    def get_like_count(self, obj):
        return obj.get_like_count()
    get_like_count.short_description = 'Likes'
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    get_comment_count.short_description = 'Comments'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at', 'get_posts_count']
    list_filter = ['created_at']
    search_fields = ['user__username', 'bio', 'location']
    
    def get_posts_count(self, obj):
        return obj.get_posts_count()
    get_posts_count.short_description = 'Posts Count'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)