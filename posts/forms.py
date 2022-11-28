from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Subreddit, Post, Comment

class SubredditForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['subreddit_name', 'subreddit_info']
        labels = {
            'subreddit_name': _(''),
            'subreddit_info': _('')
        }
        widgets = {
            'subreddit_name': forms.TextInput(attrs={
                'placeholder': 'Enter subreddit name',
                'class': 'form-control form-subreddit-name bg-textbox border border-border text-body',
            }),
            'subreddit_info': forms.Textarea(attrs={
                'placeholder': 'Add a short description (optional)',
                'class': 'form-control form-subreddit-info bg-textbox border border-border text-body',
            })
        }
        error_messages = {'subreddit_name': {'unique': 'A subreddit with this name already exists.'}}

class SubredditEditInfoForm(forms.ModelForm):
    class Meta:
        model = Subreddit
        fields = ['subreddit_info']
        widgets = {
            'subreddit_info': forms.Textarea(attrs={
                'placeholder': 'Add a short description (optional)',
                'class': 'form-control form-subreddit-info bg-textbox border border-border text-body',
            })
        }

class SubredditEditModeratorsForm(forms.Form):

    new_moderator = forms.CharField(max_length=20, label=_(''), widget=forms.TextInput(attrs={'placeholder': 'Add moderator','class': 'form-control bg-textbox border border-border text-body',}))

    def clean_new_moderator(self):
        user = self.cleaned_data['new_moderator']
        try:
            new_moderator = User.objects.get(username=user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return new_moderator
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subreddit', 'post_title', 'post_body', 'post_image']
        labels = {
            'subreddit': _(''),
            'post_title': _(''),
            'post_body': _(''),
            'post_image': _(''),
        }
        widgets = {
            'subreddit': forms.Select(attrs={
                'class': 'form-control form-select form-subreddit bg-textbox border border-border text-body',
                }),
            'post_title': forms.Textarea(attrs={
                'class': 'form-control form-post-title bg-textbox border border-border text-body',
                'placeholder': 'Title',
                }),
            'post_body': forms.Textarea(attrs={
                'class': 'form-control form-post-body bg-textbox border border-border text-body',
                'rows': 16,
                'placeholder': 'Text (optional)',
                }),
            'post_image': forms.ClearableFileInput(attrs={
                'class': 'form-control form-post-image bg-textbox border border-border text-body',
                'onchange': 'readURL(this);'
            })
        }

    def __init__(self, *args, **kwargs):
        if 'subreddit' in kwargs:
            subreddit = kwargs.pop('subreddit')
            kwargs.update(initial={'subreddit': subreddit})
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['subreddit'].empty_label = 'Subreddit'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {'comment_text': ''}
        widgets = {'comment_text': forms.Textarea(attrs={
                    'class': 'form-control comment-form bg-post border border-border text-body w-100',
                    'rows': 4,
                    'placeholder': 'Add a comment:'
                    })
        }
