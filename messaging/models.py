from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
import timeago 

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
