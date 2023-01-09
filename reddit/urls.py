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
    path('notifications/', views.notifications_view, name='notifications'),
    # ACCOUNTS
    path('login/', uviews.login_view, name='login'),
    path('logout/', uviews.logout_view, name='logout'),
    path('register/', uviews.register, name='register'),
    # HOME
    path('', views.home_view, name='home', kwargs={'sort': None}),
    path('new/', views.home_view, name='home_new', kwargs={'sort': '-created_at'}),
    path('top/', views.home_view, name='home_top', kwargs={'sort': '-score'}),
    path('submit/', views.post_create, name='home_submit', kwargs={'subreddit_url': None}),
    # PROFILE
    path('u/<slug:user>/', views.profile_view, name='profile', kwargs={'filter': None, 'sort': None}),
    path('u/<slug:user>/new/', views.profile_view, name='profile_new', kwargs={'filter': None, 'sort': 'created_at'}),
    path('u/<slug:user>/top/', views.profile_view, name='profile_top', kwargs={'filter': None, 'sort': 'score'}),
    path('u/<slug:user>/posts/', views.profile_view, name='profile_posts', kwargs={'filter': 'user.posts.all()', 'sort': None}),
    path('u/<slug:user>/posts/new/', views.profile_view, name='profile_posts_new', kwargs={'filter': 'user.posts.all()', 'sort': '-created_at'}),
    path('u/<slug:user>/posts/top/', views.profile_view, name='profile_posts_top', kwargs={'filter': 'user.posts.all()', 'sort': '-score'}),
    path('u/<slug:user>/comments/', views.profile_view, name='profile_comments', kwargs={'filter': 'user.comments.all()', 'sort': None}),
    path('u/<slug:user>/comments/new/', views.profile_view, name='profile_comments_new', kwargs={'filter': 'user.comments.all()', 'sort': '-created_at'}),
    path('u/<slug:user>/comments/top/', views.profile_view, name='profile_comments_top', kwargs={'filter': 'user.comments.all()', 'sort': '-score'}),
    # SUBREDDIT
    path('subreddit/create/', views.subreddit_create, name='subreddit_create'),
    path('r/', views.SubredditIndexView.as_view(), name='subreddit_index'),
    path('r/<slug:subreddit_url>/', views.subreddit_view, name='subreddit', kwargs={'sort': None}),
    path('r/<slug:subreddit_url>/new/', views.subreddit_view, name='subreddit_new', kwargs={'sort': '-created_at'}),
    path('r/<slug:subreddit_url>/top/', views.subreddit_view, name='subreddit_top', kwargs={'sort': '-score'}),
    path('r/<slug:subreddit_url>/edit/', views.subreddit_edit_info, name='subreddit_edit_info'),
    path('r/<slug:subreddit_url>/moderators/', views.subreddit_edit_moderators, name='subreddit_edit_moderators'),
    # POST
    path('r/<slug:subreddit_url>/submit/', views.post_create, name='post_create'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/', views.post_detail, name='post_detail', kwargs={'comment_id': None}),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/', views.vote, name='post_vote', kwargs={'comment_id': None}),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/delete/', views.post_delete, name='post_delete'),
    # COMMENT
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/<int:comment_id>/', views.vote, name='comment_vote'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/comment/<int:comment_id>/', views.post_detail, name='comment_view'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]

urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)