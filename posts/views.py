from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Subreddit, Post, Comment
from .forms import SubredditForm, PostForm, CommentForm, MessageForm

from itertools import chain
from operator import attrgetter

class SubredditIndexView(generic.ListView):
    model = Subreddit
    template_name = 'posts/subreddit_index.html'

def home_view(request, filter):
    posts = Post.objects.all()
    if filter:
        posts = posts.order_by(filter)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/home.html', {'page_obj': page_obj})

def subreddit_view(request, subreddit_url, filter):
    subreddit = get_object_or_404(Subreddit, url=subreddit_url)
    posts = subreddit.posts.all()
    if filter:
        posts = posts.order_by(filter)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/subreddit_view.html', {'subreddit': subreddit, 'page_obj': page_obj})

@login_required(login_url='/login/')
def subreddit_create(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.created_by = request.user
            subreddit.save()
            return HttpResponseRedirect(reverse('subreddit', args=[subreddit.url]))
    else:
        form = SubredditForm()
    return render(request, 'posts/subreddit_create.html', {'form': form})

@login_required(login_url='/login/')
def post_create(request, subreddit_url):
    subreddit = get_object_or_404(Subreddit, url=subreddit_url)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post.url]))
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form, 'subreddit': subreddit})

def post_detail(request, post_url, subreddit_url):
    post = get_object_or_404(Post, url=post_url)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/r/%s/comments/%s/' % (subreddit_url, post_url))
        else:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.created_by = request.user
                try:
                    reply_id = int(request.POST.get('reply_id'))
                except:
                    reply_id = None
                if reply_id:
                    comment.reply = Comment.objects.get(id=reply_id)
                comment.save()
                return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post_url]))
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def post_vote(request, post_url, subreddit_url):
    post = get_object_or_404(Post, url=post_url)
    vote = request.POST.get("vote")
    if request.user.is_authenticated:
        token = request.user.id
    else:
        token = request.META['REMOTE_ADDR']
    post.add_vote(token, int(vote))
    post.score = Post.objects.get(url=post_url).vote_total
    post.save(update_fields=['score'])
    if request.META.get('HTTP_REFERER') != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('')

def comment_vote(request, post_url, subreddit_url, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    vote = request.POST.get("vote")
    if request.user.is_authenticated:
        token = request.user.id
    else:
        token = request.META['REMOTE_ADDR']
    comment.add_vote(token, int(vote))
    comment.score = Comment.objects.get(id=comment_id).vote_total
    comment.save(update_fields=['score'])
    if request.META.get('HTTP_REFERER') != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('')

def profile_view(request, user, show_posts, show_comments, filter):
    user = User.objects.get(username=user)
    posts = user.posts.all()
    comments = user.comments.all()
    if show_posts and show_comments == True:
        if filter:
            key = attrgetter(filter)
        else:
            key = attrgetter('created_at')
        result = sorted(chain(list(posts), list(comments)), key=key, reverse=True)
    elif show_posts == True:
        if filter:
            result = posts.order_by(filter)
        else:  
            result = posts
    elif show_comments == True:
        if filter:
            result = comments.order_by(filter)
        else:
            result = comments
    return render(request, 'posts/profile.html', {'user': user, 'result' : result, 'show_posts': show_posts, 'show_comments': show_comments})

@login_required(login_url='/login/')
def messages_view(request):
    user = request.user
    sent = user.sent_messages.all()
    received = user.received_messages.all()
    return render(request, 'posts/messages.html', {'user': user, 'sent': sent, 'received': received})

@login_required(login_url='/login/')
def message_create(request):
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
    return render(request, 'posts/message_create.html', {'form': form})
