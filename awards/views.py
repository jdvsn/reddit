from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Award
from .forms import AwardSendForm

@login_required(login_url='/login/')
def awards_view(request):
    received_awards = Award.received_awards_count(request.user)
    sent_awards = Award.sent_awards_count(request.user)
    unsent_awards = Award.unsent_awards_count(request.user)
    return render(request, 'awards/home.html', {
        'user': request.user,
        'received_gold_awards': received_awards['gold'],
        'received_silver_awards': received_awards['silver'],
        'received_bronze_awards': received_awards['bronze'],
        'sent_gold_awards': sent_awards['gold'],
        'sent_silver_awards': sent_awards['silver'],
        'sent_bronze_awards': sent_awards['bronze'],
        'unsent_gold_awards': unsent_awards['gold'],
        'unsent_silver_awards': unsent_awards['silver'],
        'unsent_bronze_awards': unsent_awards['bronze'],
        })

@login_required(login_url='/login/')
def awards_send(request):
    unsent_awards = Award.unsent_awards_count(request.user)
    if request.method == 'POST':
        award_form = AwardSendForm(data=request.POST, user=request.user)
        if award_form.is_valid():
            award = Award.get_unsent_award(request.user, award_form.cleaned_data['award_tier'])
            award.sent_to = User.objects.get(id=award_form.cleaned_data['recipient'])
            award.save()
            return HttpResponseRedirect(reverse('awards_send'))
    else:
        award_form = AwardSendForm(user=request.user)

    return render(request, 'awards/send.html', {
        'user': request.user,
        'unsent_awards': unsent_awards['total'],
        'unsent_gold_awards': unsent_awards['gold'],
        'unsent_silver_awards': unsent_awards['silver'],
        'unsent_bronze_awards': unsent_awards['bronze'],
        'award_form': award_form
        })

@login_required(login_url='/login/')
def awards_detail(request):
    pass
    
