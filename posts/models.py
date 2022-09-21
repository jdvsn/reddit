from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import datetime, timezone
import timeago

class Subreddit(models.Model):
    class Meta:
        ordering = ['subreddit_name']
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subreddit_name = models.CharField(max_length=20, unique=True)
    url = models.SlugField()

    def sorted_new(self):
        return self.posts.all().order_by('-created_at')

    def sorted_top(self):
        return self.posts.all().order_by('-score')

    def save(self, *args, **kwargs):
        self.url = slugify(self.subreddit_name)
        super(Subreddit, self).save(*args, **kwargs)

    def __str__(self):
        return self.subreddit_name

class Post(models.Model):
    class Meta:
        ordering = ['-created_at']
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    subreddit = models.ForeignKey(Subreddit, related_name='posts', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=50)
    post_body = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    url = models.SlugField()
    
    def when(self):
        now = datetime.now(timezone.utc)
        date = self.created_at
        return timeago.format(date, now)

    def comment_count(self):
        return len(self.comments.all())

    def preview(self):
        if len(self.post_body) > 200:
            return self.post_body[:197] + '...'
        else:
            return self.post_body

    def save(self, *args, **kwargs):
        self.url = slugify(self.post_title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.post_title
    
class Comment(models.Model):
    class Meta:
        ordering = ['-created_at']
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)

    def when(self):
        now = datetime.now(timezone.utc)
        date = self.created_at
        return timeago.format(date, now)

    def __str__(self):
        return self.comment_text  