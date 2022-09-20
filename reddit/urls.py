from django.contrib import admin
from django.urls import path
from posts import views
from accounts import views as uviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('new/', views.HomeNewView.as_view(), name='home_new'),
    path('top/', views.HomeTopView.as_view(), name='home_top'),
    path('login/', uviews.login_view, name='login'),
    path('logout/', uviews.logout_view, name='logout'),
    path('register/', uviews.register, name='register'),
    path('subreddits/create/', views.subreddit_create, name='subreddit_create'),
    path('r/', views.SubredditIndexView.as_view(), name='subreddit_index'),
    path('r/<slug:url>/', views.SubredditView.as_view(), name='subreddit'),
    path('r/<slug:url>/new', views.SubredditNewView.as_view(), name='subreddit_new'),
    path('r/<slug:url>/top', views.SubredditTopView.as_view(), name='subreddit_top'),
    path('r/<slug:subreddit_url>/submit/', views.post_create, name='post_create'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/', views.post_detail, name='post_detail'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/', views.post_vote, name='post_vote'),
    path('r/<slug:subreddit_url>/comments/<slug:post_url>/vote/<int:comment_id>/', views.comment_vote, name='comment_vote')
]

urlpatterns += staticfiles_urlpatterns()