from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from datetime import datetime, timezone
import timeago 

class Subreddit(models.Model):
    class Meta:
        ordering = ['subreddit_name']
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subreddit_name = models.CharField(max_length=20, unique=True)
    url = models.SlugField()

    def save(self, *args, **kwargs):
        self.url = slugify(self.subreddit_name)
        super(Subreddit, self).save(*args, **kwargs)

    def __str__(self):
        return self.subreddit_name

class Post(models.Model):
    class Meta:
        ordering = ['-created_at']
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, related_name='posts', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=50)
    post_image = models.ImageField(blank=True, upload_to='posts', null=True)
    post_body = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    url = models.SlugField(max_length=55)
    
    def type(self):
        return 'post'

    def when(self):
        now = datetime.now(timezone.utc)
        date = self.created_at
        return timeago.format(date, now)

    def comment_count(self):
        return len(self.comments.all())

    def preview(self):
        if len(self.post_body) > 200:
            return self.post_body[:197] + '...'
        return self.post_body

    def save(self, *args, **kwargs):
        self.url = slugify('%s-%s' % (get_random_string(4, '123456789'), self.post_title))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return 'Post with id %s by %s to %s "%s"' % (self.id, self.created_by, self.subreddit, self.post_title)
    
class Comment(models.Model):
    class Meta:
        ordering = ['-created_at']
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
        
    def type(self):
        return 'comment'

    def when(self):
        now = datetime.now(timezone.utc)
        date = self.created_at
        return timeago.format(date, now)

    def preview(self):
        if len(self.comment_text) > 100:
            return self.comment_text[:97] + '...'
        return self.comment_text

    def __str__(self):
        return 'Comment with id %s by %s on post with id %s "%s"' % (self.id, self.created_by, self.post.id, self.post.post_title)  

class Message(models.Model):
    class Meta:
        ordering = ['-created_at']
    id = models.AutoField(primary_key=True)
    sent_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def when(self):
        now = datetime.now(timezone.utc)
        date = self.created_at
        return timeago.format(date, now)

    def __str__(self):
        return 'Message with id %s sent from %s to %s' % (self.id, self.sent_by, self.sent_to)