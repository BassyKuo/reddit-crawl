import	urllib,urllib2
import	json
import	requests
import	datetime
#from pprint import pprint

from Reddit_crawler import RedditObj

filename ='data/reddit_nosleep_1204.json'
article_old = RedditObj()
article_old.readJSON(filename)
#print article_old.dic['articles']

obj = RedditObj('http://www.reddit.com/r/nosleep/', 0 ,'')
obj.url2json(obj.next_url)
obj.get_content(0,obj.count)
obj.next_page()
print "===New keys==="
print obj.dic['articles'].keys()
print "===Old keys==="
print article_old.dic['articles'].keys()

print "===Update keys==="
article_old.update(obj.dic['articles'])
print article_old.dic['articles'].keys()
