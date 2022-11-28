from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message_text']
        labels = {
            'recipient': (''),
            'message_text': (''),
        }
        widgets = {
            'message_text': forms.Textarea(attrs={
                'placeholder': 'Message',
                'class': 'form-control bg-textbox border border-border text-body',
            })
        }

    recipient = forms.CharField(max_length=20, label=(''), widget=forms.TextInput(attrs={'placeholder': 'Recipient','class': 'form-control bg-textbox border border-border text-body'}))

    def clean_recipient(self):
        recipient_user = self.cleaned_data['recipient']
        try:
            recipient = User.objects.get(username=recipient_user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return recipient.id
    
    field_order = ['recipient', 'message_text']