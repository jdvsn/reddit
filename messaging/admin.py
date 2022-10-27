from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    fields = ['sent_by', 'sent_to', 'message_text']
admin.site.register(Message, MessageAdmin)
