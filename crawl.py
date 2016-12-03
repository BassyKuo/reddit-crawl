import	urllib,urllib2
import	json
import	requests
import	datetime
#from pprint import pprint

import os
import sys

"""
Reddit Articles Object
"""
class RedditObj:
	def __init__ (self, domain='http://www.reddit.com/r/nosleep/', count=0, name=''):
		"""
		dic = {
				'domain' : 'http://www.reddit.com/r/nosleep/', 
				'next_count' : 75,
				'next_name' : 'ttrr4'
				'next_url' : 'http://www.reddit.com/r/nosleep/.json?count=75&after=ttrr4'
				'articles' : {
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
				}
		"""
		self.domain = domain
		self.next_count = count
		self.next_name = name
		self.next_url = self.domain + ".json?count=" + str(self.next_count) + "&after=" + self.next_name
		self.dic = {'domain':self.domain, 'next_count':self.next_count, 'next_name':self.next_name, 'next_url':self.next_url, 'articles':{}}
		self.key_list = ['title', 'link_flair_text', 'score', 'ups', 'created_utc', 'edited', 'num_comments', 'selftext', 'media', 'over_18', 
						 'domain', 'subreddit', 'url', 'name']

	def url2json (self, url):
		self.url = url
		request = urllib2.Request(url)
		request.add_header( "User-Agent",         
				"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
		respond = urllib2.urlopen(request)
		self.contents = json.loads(respond.read())
		self.count = len(self.contents['data']['children'])
		self.after = self.contents['data']['after']
		return self.contents

	def next_page (self):
		try:
			count = self.next_count + 25
			name = self.after
			url = self.domain + ".json?count=" + str(count) + "&after=" + name
		except TypeError:
			return -1
		self.next_count = count
		self.next_name = name
		self.next_url = url
		return self.next_url

	def get_content (self, start=0, end=0):
		if end == 0:
			end = start + 1
		elif end > self.count or end <= start:
			print "Error: start < `end' <= count"
			return -1
		dic = {}
		#print "start: " +  str(start)
		#print "end: " + str(end)
		for num in range(start, end):
			author = self.contents['data']['children'][num]['data']['author']
			a_id = self.contents['data']['children'][num]['data']['id']
			dic[author] = {}
			dic[author][a_id] = {}
			for k in self.key_list:
				dic[author][a_id][k] = self.contents['data']['children'][num]['data'][k]
			#print dic
		self.update(dic)
		return dic

	def writeJSON(self, filename="reddit.json", dic={}):
		self.dic['next_count'] = self.next_count
		self.dic['next_name'] = self.next_name
		self.dic['next_url'] = self.domain + ".json?count=" + str(article.next_count) + "&after=" + article.next_name
		if dic=={}:
			dic = self.dic
		with open(filename, 'w') as outfile:
			json.dump(dic, outfile, ensure_ascii=True)
		outfile.close()

	def readJSON(self, filename="reddit.json"):
		with open(filename, 'r') as infile:
			self.dic = json.loads(infile.read())
		self.domain = self.dic['domain']
		self.next_count = self.dic['next_count']
		self.next_name = self.dic['next_name']
		self.next_url = self.dic['next_url']
		infile.close()
		return self.dic

	def update (self, new_dic):
		for author in new_dic.keys():
			if self.dic['articles'].has_key(author) == False:
				self.dic['articles'][author] = {}
			self.dic['articles'][author].update(new_dic[author])


if __name__ == '__main__':
	year  = datetime.date.today().timetuple()[0]
	month = datetime.date.today().timetuple()[1]
	day   = datetime.date.today().timetuple()[2]
	week  = datetime.date.today().isoweekday()
	calendar_week = datetime.date.today().isocalendar()[1]
	program = sys.argv[0]
	domain = sys.argv[1]
	pages = sys.argv[2]
	#filename = os.path.join('data', "reddit_%s_%02d%02d.json" % (domain.split('/')[4], month, day))
	filename = os.path.join('data', "reddit_%s.json" % (domain.split('/')[4]))

	if os.path.isdir('data') is False:
		os.makedirs('data')

	if os.path.exists(filename) is True:
		article = RedditObj()
		article.readJSON(filename)
	else:
		domain = "https://www.reddit.com/r/nosleep/"
		article = RedditObj(domain, 0, '')

	for n in range(0,int(pages)):
		article.url2json(article.next_url)
		article.get_content(0,article.count)
		nurl = article.next_page()
		if nurl == -1:
			break
		print nurl
		
	article.writeJSON(filename)
	


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
