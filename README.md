This is my recreation of the website [Reddit](https://www.reddit.com/). The current production site is [here](http://jreddit.joedavison.uk). If you don't know what reddit is, its essentially a forum website with user created and managed sub-forums called 'subreddits'. 

## Core functionality

 - Subreddits (sub-forums)
 - Posts
 - Comments

The core functionality is users submitting posts containing text/images to subreddits - and commenting on those posts. Posts and comments can also be upvoted or downvoted, with a visible score change. 

Any user can create a subreddit and moderate it through deleting posts and comments - the subreddit creator can also appoint/remove other users as moderators.  

Core functionality [models](https://github.com/jdvsn/reddit/blob/master/posts/models.py) and [views](https://github.com/jdvsn/reddit/blob/master/posts/views.py).

## Extra features
 - Messaging ([models](https://github.com/jdvsn/reddit/blob/master/messaging/models.py) and [views](https://github.com/jdvsn/reddit/blob/master/messaging/views.py))
 - Awards ([models](https://github.com/jdvsn/reddit/blob/master/awards/models.py) and [views](https://github.com/jdvsn/reddit/blob/master/awards/views.py))