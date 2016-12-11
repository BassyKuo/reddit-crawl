# reddit-crawl

Welcome to use REDDIT-CRAWL to crawl your own reddit.

With this tool, each data you crawled came from 3 types of url in [https://www.reddit.com/](https://www.reddit.com/):

1. https://www.reddit.com/r/{subreddit}
2. https://www.reddit.com/r/{subreddit}/comments/{article_id}
3. https://www.reddit.com/user/{username}/submitted

# Usage
For crawling the overview subreddit page:
```
python Reddit_crawler.py https://www.reddit.com/r/{subreddit} <stroage_folder>
```
For crawling the user submitted page:
```
python Reddit_user_crawler.py <username> <storage_folder>
```

or if you want to crawl a large amonut of data at once, follow here:
```
chmod +x RedditDigger*.sh
./RedditDigger.sh <subreddit_list> 
./RedditDiggerUsers.sh <user_list> [<name_expr_pattern>]
```

### For example:
```
python Reddit_crawler.py https://www.reddit.com/r/jokes/ data/
python Reddit_user_crawler.py zzz0404 data/
./RedditDigger.sh reddit_subreddit.txt
./RedditDiggerUsers.sh reddit_users.txt ^zzz     # script will find the user name match '^zzz', ex: zzz0404
```

# API
You can also use API directly in `Reddit_crawler.py`:
```
python
>>> from Reddit_crawler import *
>>>
```
It provides two classes for user, `RedditObj` and `RedditUser`, you can use `help(RedditObj)` `help(RedditUser)` to get more information:
```
>>> help(RedditObj)
>>> help(RedditUser)
>>>
```
