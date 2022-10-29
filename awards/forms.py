from django import forms
from django.contrib.auth.models import User

from .models import Award

class AwardSendForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AwardSendForm, self).__init__(*args, **kwargs)
        self.fields['award_tier'].choices = Award.send_form_choices(self.user)
    
    award_tier = forms.ChoiceField()
    recipient = forms.CharField(max_length=20)

    def clean_recipient(self):
        recipient_user = self.cleaned_data['recipient']
        try:
            recipient = User.objects.get(username=recipient_user)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        if recipient == self.user:
            raise forms.ValidationError('You cannot send an award to yourself')
        return recipient.id

