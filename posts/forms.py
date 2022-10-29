from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Subreddit, Post, Comment

class SubredditForm(ModelForm):
    class Meta:
        model = Subreddit
        fields = ['subreddit_name', 'subreddit_info']
        labels = {
            'subreddit_name': _('Create a new subreddit:'),
            'subreddit_info': _('')
        }
        widgets = {
            'subreddit_name': TextInput(attrs={
                'placeholder': 'Enter subreddit name',
                }),
            'subreddit_info': Textarea(attrs={
                'placeholder': 'Add a short description (optional)'
            })
        }
        error_messages = {'subreddit_name': {'unique': 'A subreddit with this name already exists.'}}

class SubredditEditForm(ModelForm):
    class Meta:
        model = Subreddit
        fields = ['subreddit_info']

    new_moderator = forms.CharField(max_length=20, required=False)
    remove_moderator = forms.CharField(max_length=20, required=False)

    def clean_new_moderator(self):
        user = self.cleaned_data['new_moderator']
        if user == '':
            return None
        try:
            new_moderator = User.objects.get(username=user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return new_moderator

    def clean_remove_moderator(self):
        user = self.cleaned_data['remove_moderator']
        if user == '':
            return None
        try:
            remove_moderator = User.objects.get(username=user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return remove_moderator
    
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
