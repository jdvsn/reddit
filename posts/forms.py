from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Message, Subreddit, Post, Comment

class SubredditForm(ModelForm):
    class Meta:
        model = Subreddit
        fields = ['subreddit_name']
        labels = {'subreddit_name': _('Create a new subreddit:')}
        widgets = {
            'subreddit_name': TextInput(attrs={
                'placeholder': 'Enter subreddit name',
                })
            }
        error_messages = {'subreddit_name': {'unique': 'A subreddit with this name already exists.'}}

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['subreddit', 'post_title', 'post_body', 'post_image']
        labels = {
            'post_title': _(''),
            'post_body': _(''),
            'post_image': _(''),
        }
        widgets = {
            'post_title': Textarea(attrs={
                'cols': 60, 'rows': 1,
                'placeholder': 'Title your post:'
                }),
            'post_body': Textarea(attrs={
                'cols': 80, 'rows': 20,
                'placeholder': 'Enter post text:'
                })
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {'comment_text': ''}
        widgets = {'comment_text': Textarea(attrs={
                    'cols': 125, 'rows': 4,
                    'placeholder': 'Add a comment:'
                    })
        }

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
