from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter

from .models import Subreddit, Post, Comment
from .forms import SubredditForm, PostForm, CommentForm, SubredditEditInfoForm, SubredditEditModeratorsForm
from awards.models import Award

class SubredditIndexView(generic.ListView):
    model = Subreddit
    template_name = 'posts/subreddit/subreddit_index.html'

def home_view(request, sort):
    posts = Post.objects.all()
    if sort:
        posts = posts.order_by(sort)
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/home.html', {'page_obj': page_obj})

def subreddit_view(request, subreddit_url, sort):
    subreddit = get_object_or_404(Subreddit, url=subreddit_url)
    posts = subreddit.posts.all()
    if sort:
        posts = posts.order_by(sort)
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/subreddit/subreddit_view.html', {'subreddit': subreddit, 'page_obj': page_obj})

@login_required(login_url='/login/')
def subreddit_create(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.created_by = request.user
            subreddit.save()
            subreddit.moderators.add(request.user)
            return HttpResponseRedirect(reverse('subreddit', args=[subreddit.url]))
    else:
        form = SubredditForm()
    return render(request, 'posts/subreddit/subreddit_create.html', {'form': form})

@login_required(login_url='/login/')
def subreddit_edit_info(request, subreddit_url):
    subreddit = Subreddit.objects.get(url=subreddit_url)
    if request.user == subreddit.created_by:
        can_edit = True
        if request.method == 'POST':
            form = SubredditEditInfoForm(request.POST, instance=subreddit)
            if form.is_valid():
                subreddit.save(update_fields=['subreddit_info'])
                return HttpResponseRedirect(reverse('subreddit', args=[subreddit_url]))
        else:
            form = SubredditEditInfoForm(instance=subreddit)
    else:
        can_edit = False
        form = None
    return render(request, 'posts/subreddit/subreddit_edit_info.html', {'form': form, 'subreddit': subreddit, 'can_edit': can_edit})

@login_required(login_url='/login/')
def subreddit_edit_moderators(request, subreddit_url):
    subreddit = Subreddit.objects.get(url=subreddit_url)
    if request.user == subreddit.created_by:
        can_edit = True
        if request.method == 'POST':
            remove_id = request.POST.get('remove')
            if remove_id:
                subreddit.moderators.remove(remove_id)
                return HttpResponseRedirect('')
            form = SubredditEditModeratorsForm(request.POST)
            if form.is_valid():
                subreddit.moderators.add(form.cleaned_data['new_moderator'])
                return HttpResponseRedirect('')
        else:
            form = SubredditEditModeratorsForm()
    else:
        can_edit = False
    return render(request, 'posts/subreddit/subreddit_edit_moderators.html', {'form': form, 'subreddit': subreddit, 'can_edit': can_edit})

@login_required(login_url='/login/')
def post_create(request, subreddit_url):
    try:
        subreddit = get_object_or_404(Subreddit, url=subreddit_url)
    except:
        subreddit = None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, subreddit=subreddit)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post.subreddit.url, post.url]))
    else:
        form = PostForm(subreddit=subreddit)
    return render(request, 'posts/post/post_create.html', {'form': form, 'subreddit': subreddit})

def post_detail(request, subreddit_url, post_url, comment_id):
    post = get_object_or_404(Post, url=post_url)
    if comment_id:
        comment = Comment.objects.get(id=comment_id)
    else:
        comment = None
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
                    parent = int(request.POST.get('parent_id'))
                except:
                    parent = None
                if parent:
                    comment.parent = Comment.objects.get(id=parent)
                comment.save()
                return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post_url]))
    else:
        comment_form = CommentForm()
    return render(request, 'posts/post/post_detail.html', {
        'post': post, 
        'comment': comment,
        'comments': post.comments.filter(parent=None), 
        'comment_form': comment_form, 
        'can_delete_post': post.can_delete(request.user),
        'can_delete_comments': post.can_delete_comments(request.user),
        })

@login_required(login_url='/login/')
def post_delete(request, subreddit_url, post_url):
    post = get_object_or_404(Post, url=post_url)
    if request.method == 'POST':
        if post.can_delete(request.user):
            post.delete()
            return HttpResponseRedirect(reverse('subreddit', args=[subreddit_url]))
    return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post_url]))

def vote(request, subreddit_url, post_url, comment_id):
    vote = request.POST.get("vote")
    if comment_id:
        object = get_object_or_404(Comment, id=comment_id)
        type = Comment
    else:
        object = get_object_or_404(Post, url=post_url)
        type = Post
    if request.user.is_authenticated:
        token = request.user.id
    else:
        token = request.META['REMOTE_ADDR']
    object.add_vote(token, int(vote))
    object.score = type.objects.get(id=object.id).vote_total
    object.save(update_fields=['score'])
    if request.META.get('HTTP_REFERER') != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect('')

@login_required(login_url='/login/')
def comment_delete(request, post_url, subreddit_url, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if comment.can_delete(request.user):
            comment.delete()
    return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post_url]))

def profile_view(request, user, filter, sort):
    user = User.objects.get(username=user)
    if filter:
        objects = eval(filter).order_by('-created_at')
        if sort:
            objects = objects.order_by(sort)  
    else:
        key = attrgetter('created_at')
        if sort:
            key = attrgetter(sort) 
        objects = sorted(chain(list(user.posts.all()), list(user.comments.all())), key=key, reverse=True)   
    paginator = Paginator(objects, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    awards = Award.received_awards_count(user)
    return render(request, 'posts/profile.html', {'user': user, 'page_obj' : page_obj, 'filter': filter, 'awards': awards})

@login_required(login_url='/login/')
def notifications_view(request):
    posts = request.user.posts.all()
    comments = request.user.comments.all()
    post_replies = []
    comment_replies = []
    for p in posts:
        for pr in p.comments.all():
            post_replies.append(pr)
    post_replies = sorted(post_replies, key=attrgetter('created_at'), reverse=True)
    for c in comments:
        for cr in c.replies.all():
            comment_replies.append(cr)
    comment_replies = sorted(comment_replies, key=attrgetter('created_at'), reverse=True)
    replies = sorted(chain(list(post_replies), list(comment_replies)), key=attrgetter('created_at'), reverse=True)
    return render(request, 'posts/notifications.html', {'replies': replies, 'count': len(replies)})