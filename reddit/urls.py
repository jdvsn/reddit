from django.contrib import admin
from django.urls import path, include
from posts import views
from accounts import views as uviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include('payments.urls')),
    path('messages/', include('messaging.urls')),
    path('awards/', include('awards.urls')),
    path('', views.home_view, name='home', kwargs={'filter': ''}),
    path('new/', views.home_view, name='home_new', kwargs={'filter': '-created_at'}),
    path('top/', views.home_view, name='home_top', kwargs={'filter': '-score'}),
    path('login/', uviews.login_view, name='login'),
    path('logout/', uviews.logout_view, name='logout'),
    path('register/', uviews.register, name='register'),
    path('subreddits/create/', views.subreddit_create, name='subreddit_create'),
    path('u/<slug:user>/', views.profile_view, name='profile', kwargs={'show_posts': True, 'show_comments': True,'filter': ''}),
    path('u/<slug:user>/new/', views.profile_view, name='profile_new', kwargs={'show_posts': True, 'show_comments': True,'filter': 'created_at'}),
    path('u/<slug:user>/top/', views.profile_view, name='profile_top', kwargs={'show_posts': True, 'show_comments': True,'filter': 'score'}),
    path('u/<slug:user>/posts/', views.profile_view, name='profile_posts', kwargs={'show_posts': True, 'show_comments': False,'filter': ''}),
    path('u/<slug:user>/posts/new/', views.profile_view, name='profile_posts_new', kwargs={'show_posts': True, 'show_comments': False,'filter': '-created_at'}),
    path('u/<slug:user>/posts/top/', views.profile_view, name='profile_posts_top', kwargs={'show_posts': True, 'show_comments': False,'filter': '-score'}),
    path('u/<slug:user>/comments/', views.profile_view, name='profile_comments', kwargs={'show_posts': False, 'show_comments': True,'filter': ''}),
    path('u/<slug:user>/comments/new/', views.profile_view, name='profile_comments_new', kwargs={'show_posts': False, 'show_comments': True,'filter': '-created_at'}),
    path('u/<slug:user>/comments/top/', views.profile_view, name='profile_comments_top', kwargs={'show_posts': False, 'show_comments': True,'filter': '-score'}),
    path('r/', views.SubredditIndexView.as_view(), name='subreddit_index'),
    path('r/<slug:subreddit_url>/', views.subreddit_view, name='subreddit', kwargs={'filter': ''}),
    path('r/<slug:subreddit_url>/edit/', views.subreddit_edit, name='subreddit_edit'),
    path('r/<slug:subreddit_url>/new/', views.subreddit_view, name='subreddit_new', kwargs={'filter': '-created_at'}),
    path('r/<slug:subreddit_url>/top/', views.subreddit_view, name='subreddit_top', kwargs={'filter': '-score'}),
    path('r/<slug:subreddit_url>/submit/', views.post_create, name='post_create'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/', views.post_detail, name='post_detail'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/', views.post_vote, name='post_vote'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/<int:comment_id>/', views.comment_vote, name='comment_vote'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/delete/', views.post_delete, name='post_delete'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/comment/<int:comment_id>/', views.comment_view, name='comment_view'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('notifications/', views.notifications_view, name='notifications')
]

urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)