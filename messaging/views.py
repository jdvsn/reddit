from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import MessageForm

@login_required(login_url='/login/')
def messages_view(request, folder):
    user = request.user
    if folder == 'received':
        messages = user.received_messages.all()
    elif folder =='sent':
        messages = user.sent_messages.all()
    paginator = Paginator(messages, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'messages/home.html', {'user': user,'folder': folder, 'page_obj': page_obj})

@login_required(login_url='/login/')
def messages_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sent_by = request.user
            message.sent_to = User.objects.get(id=form.cleaned_data['recipient'])
            message.save()
            return HttpResponseRedirect(reverse('messages'))
    else: 
        form = MessageForm()
    return render(request, 'messages/create.html', {'form': form})
