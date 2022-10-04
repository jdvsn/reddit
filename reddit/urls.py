from django.contrib import admin
from django.urls import path
from posts import views
from accounts import views as uviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home', kwargs={'filter': ''}),
    path('new/', views.home_view, name='home_new', kwargs={'filter': 'new'}),
    path('top/', views.home_view, name='home_top', kwargs={'filter': 'top'}),
    path('login/', uviews.login_view, name='login'),
    path('logout/', uviews.logout_view, name='logout'),
    path('register/', uviews.register, name='register'),
    path('subreddits/create/', views.subreddit_create, name='subreddit_create'),
    path('r/', views.SubredditIndexView.as_view(), name='subreddit_index'),
    path('r/<slug:subreddit_url>/', views.subreddit_view, name='subreddit', kwargs={'filter': ''}),
    path('r/<slug:subreddit_url>/new/', views.subreddit_view, name='subreddit_new', kwargs={'filter': 'new'}),
    path('r/<slug:subreddit_url>/top/', views.subreddit_view, name='subreddit_top', kwargs={'filter': 'top'}),
    path('r/<slug:subreddit_url>/submit/', views.post_create, name='post_create'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/', views.post_detail, name='post_detail'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/', views.post_vote, name='post_vote'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/<int:comment_id>/', views.comment_vote, name='comment_vote')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)