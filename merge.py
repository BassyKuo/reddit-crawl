from Reddit_crawler import *
import os, sys

if __name__ == '__main__':
    subreddit = sys.argv[1]

    old = RedditObj()
    new = RedditObj()
    old.readJSON ("data_summary/reddit_%s_summary.json" % subreddit)
    new.readJSON ("data/_summary/reddit_%s_summary.json" % subreddit)
    old.update (new.dic['articles'])
    new.dic['articles'] = old.dic['articles']
    new.writeJSON ("data_summary/reddit_%s_summary.json" % subreddit)
