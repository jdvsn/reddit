from django.contrib import admin

from .models import Subreddit, Post, Comment, Message

class SubredditAdmin(admin.ModelAdmin):
    fields = ['subreddit_name']
admin.site.register(Subreddit, SubredditAdmin)

class PostAdmin(admin.ModelAdmin):
    fields = ['created_by','subreddit', 'post_title', 'post_body']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    fields = ['created_by','post', 'comment_text']
admin.site.register(Comment, CommentAdmin)

class MessageAdmin(admin.ModelAdmin):
    fields = ['sent_by', 'sent_to', 'message_text']
admin.site.register(Message, MessageAdmin)

# class CommentReplyAdmin(admin.ModelAdmin):
#     fields =['comment', 'reply_text']
# admin.site.register(CommentReply, CommentReplyAdmin)
