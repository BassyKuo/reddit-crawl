import	urllib,urllib2
import	json
import	requests
import	datetime
#from pprint import pprint

import os
import sys

def url2json (url):
	try:
		request = urllib2.Request(url)
		request.add_header( "User-Agent",
							"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
		respond = urllib2.urlopen(request)
		contents = json.loads(respond.read())
		# self.page_len = len(self.contents['data']['children'])
		# self.after = self.contents['data']['after']
		return contents
	except urllib2.HTTPError, e:
		if '404' in str(e) or '403' in str(e):
			return -1
		print "urllib2.HTTPError: %s caused error. Try again." % url
		return url2json(url)

class RedditComment:
	"""
	< Reddit Articles Comments>
	Usage:
	  obj = RedditComment('https://www.reddit.com/r/Patriots/comments/1clnp4/posting_here_hoping_it_might_gain_traction/.json')
	  obj.url2json(obj.next_url)
	  obj.get_content(0, obj.page_len)
	  obj.next_page()
	  obj.get_content(0, obj.page_len)
	  obj.next_page()
	  obj.writeJSON('reddit_jokes_output.json')
	----------------------------------------------------
	"""
	def __init__ (self, url):
		"""
		x = RedditComment('https://www.reddit.com/r/AskReddit/comments/4ue58r/.json')

		Init:	dic, url, subreddit, a_id, key_list, comm_list
		[*] dic = {
				....,
				'articles' : {
					"$username_1" : {
						"$article_id_1" : { 'title' , 'link_flair_text' , 'score' , 'ups' , 
											'created_utc' , 'edited' , 'num_comments' , 'selftext' , 'preview' , 
											'media' , 'over_18' , 'domain' , 'subreddit' , 'url' , 'name' ,
											'comments' : {
											   '$comment_name_1': {
													'level' : '2',
													'author' : Amy,
													'parent_id' : 't1_tt776',
													....
											   },
											   '$comment_name_2': {
													'level' : '1',
													'author' : Judy,
													'parent_id' : 't1_tt87j',
													....
											   },...
											}
						},...
					},...
				}
		    }
		"""
		"""
		Content:	content[0]
		Comments:	content[1]
			>> contents[1]['data']['children'][0]['data'].keys():
			[u'subreddit_id', u'banned_by', u'removal_reason', u'link_id', u'likes', u'replies', u'user_reports', u'saved', u'id', u'gilded', u'archived', u'report_reasons', u'author', u'parent_id', u'score', u'approved_by', u'controversiality', u'body', u'edited', u'author_flair_css_class', u'downs', u'body_html', u'subreddit', u'name', u'score_hidden', u'stickied', u'created', u'author_flair_text', u'created_utc', u'distinguished', u'mod_reports', u'num_reports', u'ups']
		"""
		if urlparse(url).path.split('/')[-1] != ".json":
			url = url + ".json"
		self.subreddit = urlparse(url).path.split('/')[2]
		self.a_id = urlparse(url).path.split('/')[4]
		# self.domain = domain
		# self.a_count = 0
		# self.next_count = count
		# self.next_name = name
		# self.next_url = self.domain + ".json?count=" + str(self.next_count) + "&after=" + self.next_name
		self.dic = {'articles':{}}
		self.key_list = ['title', 'link_flair_text', 'score', 'ups', 'created_utc', 'edited', 'num_comments', 'selftext', 'preview', 
						 'media', 'over_18', 'domain', 'subreddit', 'url', 'name']
		self.comm_list = ['banned_by', 'removal_reason', 'link_id', 'likes', 'user_reports', 'gilded', 'archived', 'report_reasons', 'author', 
						 'parent_id', 'score', 'approved_by', 'controversiality', 'body', 'edited', 'downs', 'subreddit', 'name', 
						 'score_hidden', 'stickied', 'created', 'created_utc', 'distinguished', 'mod_reports', 'num_reports', 'ups']

	def url2json (self, url):
		"""
		x.url2json(url)    -- return json_content
		"""
		request = urllib2.Request(url)
		request.add_header( "User-Agent",
							"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
		respond = urllib2.urlopen(request)
		self.contents = json.loads(respond.read())
		self.comment_count = len(self.contents[1]['data']['children'])
		self.subreddit = urlparse(url).path.split('/')[2]
		self.a_id = urlparse(url).path.split('/')[4]
		return self.contents

	def fetch (self):
		dic = {'articles': {}}
		try:
			""" fetch content """
			id, num = 0, 0
			author = self.contents[id]['data']['children'][num]['data']['author']
			a_id = self.contents[id]['data']['children'][num]['data']['id']
			dic['articles'][author] = {}
			dic['articles'][author][a_id] = {}
			for k in self.key_list:
				if self.contents[id]['data']['children'][num]['data'].has_key(k) is True:
					dic['articles'][author][a_id][k] = self.contents[id]['data']['children'][num]['data'][k]
				else:
					dic['articles'][author][a_id][k] = None
			""" fetch comments """
			id, level = 1, 0
			for comm in range(0,self.comment_count):
				c_name = self.contents[id]['data']['children'][comm]['data']['name']
				
			self.update(dic['articles'])
		except IndexError:
			print "Failed: `%s is empty." % self.url
			return -1

	def fetch_comment (self, level, dic):
			level += 1
			num += 1
			reply = {}
			for num in range(0, len(dic['data']['replies']['data']['children'])):
				c_name = dic['data']['replies']['data']['children'][num]['data']['name']
				if reply.has_key(c_name) is False:
					reply[c_name] = {}
				for item in comm_list:
					reply[c_name][item] = dic['data']['replies']['data']['children'][num]['data'][item]
				reply[c_name]['level'] = level

	def get_content (self, id):
		"""
		x.get_content(0)         # return content
		x.get_content(1)         # return comments
		    -- return json_content or json_comments, and store into x.dic
		"""
		if id == 0:
		dic = {}
		for num in range(start, end):
			try:
				author = self.contents['data']['children'][num]['data']['author']
				a_id = self.contents['data']['children'][num]['data']['id']
				dic[author] = {}
				dic[author][a_id] = {}
				for k in self.key_list:
					if self.contents['data']['children'][num]['data'].has_key(k) is True:
						dic[author][a_id][k] = self.contents['data']['children'][num]['data'][k]
					else:
						dic[author][a_id][k] = None
				self.a_count += 1
			except IndexError:
				print "Failed: `%s is empty." % self.url
				return -1
		self.update(dic)
		return dic

	def list_authors (self):
		"""
		x.list_authors()    -- list all authors in RedditObj
		"""
		return self.dic['articles'].keys()

	def list_article_id (self, author):
		"""
		x.list_article_id($author)    -- list all `article_id` of $author in RedditObj
		"""
		return self.dic['articles'][author].keys()

	def list_attr (self):
		"""
		x.list_attr()    -- list all attributes(keys) in RedditObj.dic['artciles']
		"""
		return self.key_list

	def get_attr (self, author, a_id, attr):
		"""
		x.get_attr($author, $a_id, $attr)    -- return the value in RedditObj.dic['articles'][$author][$a_id][$attr] 
		"""
		return self.dic['articles'][author][a_id][attr]

	def writeJSON (self, filename="reddit.json", dic={}):
		"""
		x.writeJSON($filename)    -- write RedditObj in the file
		"""
		self.dic['next_count'] = self.next_count
		self.dic['next_name'] = self.next_name
		self.dic['next_url'] = self.domain + ".json?count=" + str(article.next_count) + "&after=" + self.next_name
		if dic=={}:
			dic = self.dic
		with open(filename, 'w') as outfile:
			json.dump(dic, outfile, ensure_ascii=True)
		outfile.close()

	def readJSON(self, filename="reddit.json"):
		"""
		x.readJSON($filename)    -- read the file into RedditObj
		"""
		with open(filename, 'r') as infile:
			self.dic = json.loads(infile.read())
			self.domain = self.dic['domain']
			self.next_count = self.dic['next_count']
			self.next_name = self.dic['next_name']
			self.next_url = self.dic['next_url']
			infile.close()
		return self.dic

	def update (self, new_dic):
		"""
		x.update($new_dic['articles'])    -- update this RedditObj articles information 
		                                     if new_dic = {'articles': 
		                                                       '$author1': { '$a_id11':..., '$a_id12':... },
		                                                       '$author2': {....}, ... 
		                                                  }                       
		"""
		for author in new_dic.keys():
			if self.dic['articles'].has_key(author) == False:
				self.dic['articles'][author] = {}
			self.dic['articles'][author].update(new_dic[author])

class RedditUser:
	"""
	< Reddit Users Object >
	Usage:
	 obj = RedditUser(username)
	 obj.url2json(obj.next_url)
	 obj.get_content(0, obj.page_len)
	 obj.next_page()
	 obj.get_content(0, obj.page_len)
	 obj.next_page()
	 obj.writeJSON('reddit_user_output.json')
	"""
	def __init__ (self, user=''):
		self.user = user
		self.domain = 'https://www.reddit.com/user/' 
		self.url = self.domain + user + '/submitted/.json'
		self.a_count = 0
		self.next_count = 0
		self.next_name = ''
		self.next_url = self.domain + user + '/submitted/.json?after=' + self.next_name
		self.dic = {'domain':'USER', 'next_count':self.next_count, 'next_name':self.next_name, 'next_url':self.next_url, 'articles':{}}
		self.key_list = ['title', 'link_flair_text', 'score', 'ups', 'created_utc', 'edited', 'num_comments', 'selftext', 'preview', 
						 'media', 'over_18', 'domain', 'subreddit', 'url', 'name']
		""" [EX] 'subreddit' : nosleep / jokes / NoSleepOOC, ..... """

	def url2json (self, url):
		try:
			self.url = url
			request = urllib2.Request(url)
			request.add_header( "User-Agent",
								"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
			respond = urllib2.urlopen(request)
			self.contents = json.loads(respond.read())
			self.page_len = len(self.contents['data']['children'])
			self.after = self.contents['data']['after']
			return self.contents
		except urllib2.HTTPError:
			print "urllib2.HTTPError: %s caused error. Try again." % url
			return self.url2json(url)

	def next_page (self):
		self.next_count = self.next_count + 25
		try:
			name = self.after
			url = self.domain + self.user + "/submitted/.json?after=" + name
		except TypeError:
			return -1
		self.next_name = name
		self.next_url = url
		return self.next_url

	def get_content (self, start=0, end=0):
		if end == 0:
			end = start + 1
		elif end > self.page_len or end <= start:
			print "Error: start < `end' <= count"
			return -1
		dic = {}
		#print "start: " +  str(start)
		#print "end: " + str(end)
		for num in range(start, end):
			try:
				author = self.contents['data']['children'][num]['data']['author']
				a_id = self.contents['data']['children'][num]['data']['id']
				dic[author] = {}
				dic[author][a_id] = {}
				for k in self.key_list:
					if self.contents['data']['children'][num]['data'].has_key(k) is True:
						dic[author][a_id][k] = self.contents['data']['children'][num]['data'][k]
					else:
						dic[author][a_id][k] = None
				#print dic
				self.a_count += 1
			except IndexError:
				print "Failed: `%s is empty." % self.url
				return -1
		self.update(dic)
		return dic

	def get_authors (self):
		return self.dic['articles'].keys()

	def get_article_id (self, author):
		return self.dic['articles'][author].keys()

	def list_attr (self):
		return self.key_list

	def get_attr (self, author, a_id, attr):
		return self.dic[author][a_id][attr]

	def writeJSON (self, filename="reddit_user.json", dic={}):
		self.dic['next_count'] = self.next_count
		self.dic['next_name'] = self.next_name
		self.dic['next_url'] = self.domain + self.user + "/submitted/.json?after=" + self.next_name
		if dic=={}:
			dic = self.dic
		with open(filename, 'w') as outfile:
			json.dump(dic, outfile, ensure_ascii=True)
		outfile.close()

	def readJSON (self, filename="reddit_user.json"):
		with open(filename, 'r') as infile:
			self.dic = json.loads(infile.read())
			self.domain = self.dic['domain']
			self.next_count = self.dic['next_count']
			self.next_name = self.dic['next_name']
			self.next_url = self.dic['next_url']
			infile.close()
		return self.dic

	def update (self, new_dic):
		if new_dic.has_key('articles') is True:
			print "Failed: `new_dic should NOT have the key 'articles'."
			print "         > That is: `new_dic = { '$author_1': ..., '$author_2', ... }"
			return -1
		for author in new_dic.keys():
			if self.dic['articles'].has_key(author) is False:
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
	#pages = sys.argv[2]
	filename = os.path.join('data', "reddit_%s_%02d%02d.json" % (domain.split('/')[4], month, day))
	filename_sum = os.path.join('data', "reddit_%s_sum.json" % (domain.split('/')[4]))

	if os.path.isdir('data') is False:
		os.makedirs('data')

	article = RedditObj(domain, 0, '')

	nurl = 0
	while nurl != -1: 
		article.url2json(article.next_url)
		article.get_content(0,article.page_len)
		nurl = article.next_page()
		print nurl
	else:
		print "total: " + str(article.next_count)

	if os.path.exists(filename) is True:
		article_old = RedditObj()
		article_old.readJSON(filename)
		article_old.update(article.dic['articles'])
		article.dic['articles'] = article_old.dic['articles']

	article.writeJSON(filename)

	if os.path.exists(filename_sum) is True:
		article_old = RedditObj()
		article_old.readJSON(filename_sum)
		article_old.update(article.dic['articles'])
		article.dic['articles'] = article_old.dic['articles']

	article.writeJSON(filename_sum)

	with open('reddit_users.txt', 'a') as f:
		for user in article.get_authors():
			f.write("%s\n" % user)
	f.close()



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
		17. preview (not each subreddit has)
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
