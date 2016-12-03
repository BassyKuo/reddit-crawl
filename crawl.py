import	urllib,urllib2
import	json
import	requests
from pprint import pprint

"""
Reddit Articles Object
"""
class RedditObj:
	def __init__ (self, url):
		self.url = url
		self.url2JSON(url)
		self.dic = {}
		"""
		dic = {
				"$username_1" : {
					"$article_id_1" : { 'title' , 'link_flair_text' , 'score' , 'ups' , 
										'created_utc' , 'edited' , 'num_comments' , 'selftext' , 
										'media' , 'over_18' , 'domain' , 'subreddit' , 'url' , 'name' },
					"$article_id_2" : {...},
					},
				"$username_2" : {
					"$article_id_1" : {...},
					"$article_id_2" : {...},
					....
					},
				"$username_3"...
				}
		"""
		self.key_list = ['title', 'link_flair_text', 'score', 'ups', 'created_utc', 'edited', 'num_comments', 'selftext', 'media', 'over_18', 
						 'domain', 'subreddit', 'url', 'name']
		
	def url2JSON (self, url):
		self.url = url
		request = urllib2.Request(url)
		request.add_header( "User-Agent",         
				"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
		respond = urllib2.urlopen(request)
		self.contents = json.loads(respond.read())
		self.count = len(self.contents['data']['children'])
		self.after = self.contents['data']['after']
		#print self.contents
		#print self.count
		#print self.after
		return self.contents

	def count (self):
		return self.count

	def after (self):
		return self.after
	
	def dic (self):
		return self.dic

	def get_content (self, start=0, end=0):
		if end == 0:
			end = start + 1
		elif end > self.count or end <= start:
			print "Error: start < `end' <= count"
			return -1
		dic = {}
		print "start: " +  str(start)
		print "end: " + str(end)
		for num in range(start, end):
			author = self.contents['data']['children'][num]['data']['author']
			a_id = self.contents['data']['children'][num]['data']['id']
			dic[author] = {}
			dic[author][a_id] = {}
			for k in self.key_list:
				dic[author][a_id][k] = self.contents['data']['children'][num]['data'][k]
			print dic
		return dic

	def writeJSON(self, filename="reddit.json", dic={}):
		if dic=={}:
			dic = self.dic
		with open(filename, 'a') as outfile:
			json.dump(dic, outfile, ensure_ascii=True)

	def readJSON(self, filename="reddit.json"):
		with open(filename, 'r') as infile:
			dic = json.loads(infile.read())
		return dic

	def update (self, new_dic):
		for author in new_dic.keys():
			if self.dic.has_key(author) == False:
				self.dic[author] = {}
			self.dic[author].update(new_dic[author])


if __name__ == '__main__':
	count = 0
	domain = "https://www.reddit.com/r/nosleep/"
	url = domain + ".json"
	article = RedditObj(url)
	dic = article.get_content(0,article.count)
	article.update(dic)

	for n in range(1,30):
		count += 25
		url = domain + ".json?count=" + str(count) + "&after=" + article.after
		article.url2JSON(url)
		dic = article.get_content(0,article.count)
		article.update(dic)
	article.writeJSON("reddit_1203.json")
	


""" ======DATA TYPE======
${number} = 2..26

data['data']['children'][${number}]['data'].keys:
	1. title
	2. link_flair_text (title class)
	3. author
	4. score
	5. ups
	6. created_utc
	7. edited
	8. num_comments
	9. selftext
	10. media (influence score?)
	11. over_18 (influence score?)
	12. domain: (self.nosleep)
	13. subreddit: (no sleep)
	14. id
	15. url (not really needs, since url="reddit/r/nosleep/${id}")
	16. name ( ${kind}_${id}, ex: t3_5f8wjj )
	contest_mode
	banned_by
	selftext_html
	likes
	suggested_sort
	user_reports
	secure_media
	saved
	media_embed
	gilded
	secure_media_embed
	clicked
	report_reasons
	approved_by
	hidden
	thumbnail
	subreddit_id
	link_flair_css_class
	author_flair_css_class
	downs
	archived
	removal_reason
	stickied
	is_self
	hide_score
	spoiler
	permalink
	locked
	created
	author_flair_text
	quarantine
	mod_reports
	visited
	num_reports
	distinguished
"""

"""
Get Comment
"""
#content_url=""
#request = urllib2.Request(content_url)
#request.add_header(	"User-Agent",
#					"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
#respond = urllib2.urlopen(request)
#content = json.loads(respond.read())

### Content ####
#for key in content[0]['data']['children'][0]['data']:
#	 print "%s:\t%s"%(key,content[0]['data']['children'][0]['data'][key])
### Comments ###
#for key in content[1]['data']['children'][0..last]['data']:
#	 print "%s:\t%s"%(key,content[1]['data']['children'][0..last]['data'][key])
