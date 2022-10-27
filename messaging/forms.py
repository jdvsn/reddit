from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message_text']

    recipient = forms.CharField(max_length=20)

    def clean_recipient(self):
        recipient_user = self.cleaned_data['recipient']
        try:
            recipient = User.objects.get(username=recipient_user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return recipient.id
    
    field_order = ['recipient', 'message_text']