from django.contrib import admin

from .models import Subreddit, Post, Comment

class SubredditAdmin(admin.ModelAdmin):
    fields = ['subreddit_name']
admin.site.register(Subreddit, SubredditAdmin)

class PostAdmin(admin.ModelAdmin):
    fields = ['subreddit', 'post_title', 'post_body']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields =['post', 'comment_text']
admin.site.register(Comment, CommentAdmin)

# class CommentReplyAdmin(admin.ModelAdmin):
#     fields =['comment', 'reply_text']
# admin.site.register(CommentReply, CommentReplyAdmin)
