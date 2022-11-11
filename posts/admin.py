from django.contrib import admin

from .models import Subreddit, Post, Comment

class SubredditAdmin(admin.ModelAdmin):
    fields = ['created_by', 'subreddit_name', 'subreddit_info', 'moderators']
admin.site.register(Subreddit, SubredditAdmin)

class PostAdmin(admin.ModelAdmin):
    fields = ['created_by', 'subreddit', 'post_type', 'post_title', 'post_body']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields = ['created_by', 'post', 'comment_text']
admin.site.register(Comment, CommentAdmin)