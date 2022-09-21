from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

from .models import Subreddit, Post, Comment
from .forms import SubredditForm, PostForm, CommentForm

class HomeView(generic.ListView):
    model = Post
    template_name = 'posts/home.html'

class HomeNewView(HomeView):
    def get_queryset(self):
        return Post.objects.order_by('-created_at')

class HomeTopView(HomeView):
    def get_queryset(self):
        return Post.objects.order_by('-score')

class SubredditIndexView(generic.ListView):
    model = Subreddit
    template_name = 'posts/subreddit_index.html'

class SubredditView(generic.DetailView):
    model = Subreddit
    template_name = 'posts/subreddit_view.html'
    slug_field = 'url'
    slug_url_kwarg = 'url'

class SubredditNewView(SubredditView):
    template_name='posts/subreddit_new.html'

class SubredditTopView(SubredditView):
    template_name='posts/subreddit_top.html'

@login_required(login_url='/login/')
def subreddit_create(request):
    if request.method == 'POST':
        form = SubredditForm(request.POST)
        if form.is_valid():
            subreddit = form.save(commit=False)
            subreddit.created_by = request.user
            subreddit.save()
            url = slugify(form.cleaned_data['subreddit_name'])
            return HttpResponseRedirect(reverse('subreddit', args=[url]))
    else:
        form = SubredditForm()
    return render(request, 'posts/subreddit_create.html', {'form': form})

@login_required(login_url='/login/')
def post_create(request, subreddit_url):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            url = slugify(form.cleaned_data['post_title'])
            return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, url]))
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {
        'form': form,
        'subreddit': subreddit_url
        })

def post_detail(request, post_url, subreddit_url):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, url=post_url)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/r/%s/comments/%s/' % (subreddit_url, post_url))
        else:
            if comment_form.is_valid():
                comment = comment_form.cleaned_data['comment_text']
                reply_obj = None
                try:
                    reply_id = int(request.POST.get('reply_id'))
                except:
                    reply_id = None
                if reply_id:
                    reply_obj = Comment.objects.get(id=reply_id)
                    if reply_obj:
                        Comment(comment_text=comment, reply=reply_obj, post=post, created_by=request.user).save()
                else:
                    Comment(comment_text=comment, post=post, created_by=request.user).save()
                return HttpResponseRedirect(reverse('post_detail', args=[subreddit_url, post_url]))  
    else:
        comment_form = CommentForm()
    return render(request, template, {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
        })


def post_vote(request, post_url, subreddit_url):
    post = get_object_or_404(Post, url=post_url)
    vote = request.POST.get("vote")
    if request.user.is_authenticated:
        token = request.user.id
    else:
        token = request.META['REMOTE_ADDR']
    if vote == "up":
        post.add_vote(token, +1)
    elif vote == "down":
        post.add_vote(token, -1)
    post.score = Post.objects.get(url=post_url).vote_total
    post.save()
    if request.META.get('HTTP_REFERER') != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('')

def comment_vote(request, post_url, subreddit_url, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    vote = request.POST.get("vote")
    if request.user.is_authenticated:
        token = request.user.id
    else:
        token = request.META['REMOTE_ADDR']
    if vote == "up":
        comment.add_vote(token, +1)
    elif vote == "down":
        comment.add_vote(token, -1)
    comment.save()
    if request.META.get('HTTP_REFERER') != None:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('')
