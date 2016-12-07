import	urllib,urllib2
import	json
import	requests
import	datetime
#from pprint import pprint

import os
import sys

def url2json (url):
	"""
	content = url2json('http://www.reddit.com/r/subreddit/comments/a_id/.json')    -- return json_content
	"""
	try:
		if ('.json' in url) is False:
			url = url + '.json'
		request = urllib2.Request(url)
		request.add_header ("User-Agent",
							"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
		respond = urllib2.urlopen(request)
		content = json.loads(respond.read())
		return content
	except urllib2.HTTPError, e:
		if '404' in str(e) or '403' in str(e):
			return -1
		# elif '503' in str(e):
			# print "urllib2.HTTPError: %s timeout error. Try again." % url
		print "urllib2.HTTPError: %s caused error. Try again." % url
		return url2json(url)

def fetch_comment (comment, dic, level, num):
	"""
	comment = fetch_comment({}, content[1], 1, 0)    -- return comment part in the json_content
	
	comment = {
		"$c_name_1" : { 'level' , 'parent_id' , 'body' , ... },
		"$c_name_2" : { 'level' , 'parent_id' , 'body' , ... },
		....
	}
	"""
	if dic['data']['children'] == []:
		return {}
	c_name = dic['data']['children'][num]['data']['name']
	comment[c_name] = {}
	comment[c_name]['child_id'] = {}
	comment[c_name]['level'] = level
	# print c_name
	# print dic['data']['children'][num]['data'].keys()
	for item in dic['data']['children'][num]['data'].keys():
		if item != 'replies' and item != 'body_html':
			comment[c_name][item] = dic['data']['children'][num]['data'][item]
	# for item in comment[c_name].keys():
		# print "\t%s:\t%s" % (item, comment[c_name][item])
	if dic['data']['children'][num]['data'].has_key('replies') and dic['data']['children'][num]['data']['replies'] != '':
		comment[c_name]['child_id'] = {
			dic['data']['children'][num]['data']['replies']['data']['children'][i]['data']['name']:'' 
			for i in range(0,len(dic['data']['children'][num]['data']['replies']['data']['children']))
			}
		comment.update(fetch_comment(comment, dic['data']['children'][num]['data']['replies'], level+1, 0))
	if num+1 < len(dic['data']['children']):
		comment.update(fetch_comment(comment, dic, level, num+1))
	return comment

def urljoin (*args):
	return '/'.join(s.strip('/') for s in args)

class RedditObj:
	"""
	< Reddit Articles Object >
	Usage:
	  obj = RedditObj('http://www.reddit.com/r/jokes/')
	  obj.url2json(obj.next_url)
	  obj.get_content(0, obj.page_len)
	  obj.next_page()
	  obj.get_content(0, obj.page_len)
	  obj.next_page()
	  obj.writeJSON('reddit_jokes_output.json')
	----------------------------------------------------
	"""

	def __init__ (self, domain='http://www.reddit.com/r/nosleep/', count=0, name=''):
		"""
		Init:	dic, domain, next_count (`count` in url), next_name (`after` in url), next_url, a_count, key_list
		
		dic = {
			'domain' : 'http://www.reddit.com/r/nosleep/', 
			'next_count' : 75,
			'next_name' : 'ttrr4'
			'next_url' : 'http://www.reddit.com/r/nosleep/.json?count=75&after=ttrr4'
			'articles' : {
				"$username_1" : {
					"$article_id_1" : { 'title' , 'link_flair_text' , 'score' , 'ups' , 
					                    'created_utc' , 'edited' , 'num_comments' , 'selftext' , 'preview' , 
					                    'media' , 'over_18' , 'domain' , 'subreddit' , 'url' , 'name' },
					"$article_id_2" : {...},
				},
				"$username_2" : {
				        "$article_id_1" : {...},
				        "$article_id_2" : {...},
			        ...
			        }
				"$username_3"...
		    }
		}
		"""
		self.domain = domain
		self.a_count = 0
		self.next_count = count
		self.next_name = name
		self.next_url = self.domain + ".json?count=" + str(self.next_count) + "&after=" + self.next_name
		self.dic = {'domain':self.domain, 'next_count':self.next_count, 'next_name':self.next_name, 'next_url':self.next_url, 'articles':{}}
		self.key_list = ['title', 'link_flair_text', 'score', 'ups', 'created_utc', 'edited', 'num_comments', 'selftext', 'preview', 
						 'media', 'over_18', 'domain', 'subreddit', 'url', 'name']
		"""
		PS. the key 'preview' is NOT in every subreddits
		"""

	def url2json (self, url):
		"""
		x.url2json(x.next_url)    -- return json_content
		"""
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
		except urllib2.HTTPError, e:
			if '404' in str(e) or '403' in str(e):
				return -1
			print "urllib2.HTTPError: %s caused error. Try again." % url
			return self.url2json(url)

	def next_page (self):
		"""
		x.next_page()    -- update next page information (count, after, url), and return next_url (-1: false)
		"""
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
		"""
		x.get_content(5, 7)         # return id=5,6 contents
		x.get_content(0, x.page_len)   # return all contents
		    -- return json_content from `start` to `end`, and store in RedditObj.dic
		"""
		if end == 0:
			end = start + 1
		elif end > self.page_len or end <= start:
			print "Error: start < `end' <= page_len"
			return -1
		for num in range(start, end):
			dic = {}
			comment = {}
			try:
				author = self.contents['data']['children'][num]['data']['author']
				a_id = self.contents['data']['children'][num]['data']['id']
				# c_url = self.contents['data']['children'][num]['data']['url']
				c_url = urljoin (self.domain, "comments", a_id, ".json")
				dic[author] = {}
				dic[author][a_id] = {}
				for k in self.key_list:
					if self.contents['data']['children'][num]['data'].has_key(k) is True:
						dic[author][a_id][k] = self.contents['data']['children'][num]['data'][k]
					else:
						dic[author][a_id][k] = None
				print c_url
				commjson = url2json (c_url)
				comment = fetch_comment ({}, commjson[1], 1, 0)
				dic[author][a_id]['comments'] = comment
				self.a_count += 1
			except IndexError:
				print "Failed: %s is empty." % self.url
				return -1
		self.update(dic)
		return dic

	def authors (self):
		"""
		x.authors()    -- list all authors in RedditObj
		"""
		return self.dic['articles'].keys()

	def ids (self, author):
		"""
		x.ids(author)    -- list all `article_id` of author in RedditObj
		"""
		return self.dic['articles'][author].keys()

	def keys (self):
		"""
		x.keys()    -- list all attributes(keys) in RedditObj.dic['artciles']
		"""
		return self.key_list

	def getitem (self, author, a_id, attr):
		"""
		x.getitem(author, a_id, attr)    -- return the value in RedditObj.dic['articles'][author][a_id][attr] 
		"""
		return self.dic['articles'][author][a_id][attr]

	def setitem (self, target, value, author, a_id):
		"""
		x.setitem('comments', comm_dic, author, a_id)    -- set the target item in RedditObj.dic['articles'][author][a_id][target]
		"""
		self.dic['articles'][author][a_id][target] = value

	def writeJSON (self, filename="reddit.json", dic={}):
		"""
		x.writeJSON(filename)    -- write RedditObj in the file
		"""
		self.dic['a_count'] = self.a_count
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
		x.readJSON(filename)    -- read the file into RedditObj
		"""
		with open(filename, 'r') as infile:
			self.dic = json.loads(infile.read())
			self.domain = self.dic['domain']		 if self.dic.has_key('domain')	else None 
			self.a_count = self.dic['a_count']		 if self.dic.has_key('a_count') else None
			self.next_count = self.dic['next_count'] if self.dic.has_key('next_count')	else None
			self.next_name = self.dic['next_name'] 	 if self.dic.has_key('next_name')	else None
			self.next_url = self.dic['next_url'] 	 if self.dic.has_key('next_url')	else None
		infile.close()
		return self.dic

	def show (self):
		"""
		x.show()    -- print RedditObj.dic
		"""
		for author in self.dic['articles'].keys():
			for a_id in self.dic['articles'][author].keys():
				print "[ %s ]: %s" % (author, a_id)
				for item in self.dic['articles'][author][a_id].keys():
					if item == 'comments':
						print "\t%s:" % item
						for c_name in self.dic['articles'][author][a_id][item].keys():
							print "\t\t%s:" % c_name
							for i in self.dic['articles'][author][a_id][item][c_name].keys():
								print "\t\t\t%s:\t%s" % (i, self.dic['articles'][author][a_id][item][c_name][i])
					else:
						print "\t%s:\t%s" % (item, self.dic['articles'][author][a_id][item])


	def update (self, new_dic):
		"""
		x.update(new_dic['articles'])    -- update this RedditObj articles information 
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
		"""
		Init:	dic, domain, a_count, url, next_count (`count` in url), next_name (`after` in url), next_url, key_list

		dic = {
			'domain' : 'http://www.reddit.com/user/',
			'url' : 'http://www.reddit.com/user/Amy/submitted/.json'
			'next_count' : 75,
			'next_name' : 'ttrr4'
			'next_url' : 'http://www.reddit.com/r/nosleep/.json?count=75&after=ttrr4'
			'articles' : {
				"$username_1" : {
					"$article_id_1" : { 'title' , 'link_flair_text' , 'score' , 'ups' , 
					                    'created_utc' , 'edited' , 'num_comments' , 'selftext' , 'preview' , 
					                    'media' , 'over_18' , 'domain' , 'subreddit' , 'url' , 'name' },
					"$article_id_2" : {...},
				},
				"$username_2" : {
				        "$article_id_1" : {...},
				        "$article_id_2" : {...},
			        ...
			        }
				"$username_3"...
		    }
		}
		"""
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
		"""
		x.url2json(x.next_url)    -- return json_content
		"""
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
		except urllib2.HTTPError, e:
			if '404' in str(e) or '403' in str(e):
				return -1
			print "urllib2.HTTPError: %s caused error. Try again." % url
			return self.url2json(url)

	def next_page (self):
		"""
		x.next_page()    -- update next page information (count, after, url), and return next_url (-1: false)
		"""
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
		"""
		x.get_content(5, 7)         # return id=5,6 contents
		x.get_content(0, x.page_len)   # return all contents
		    -- return json_content from `start` to `end`, and store in RedditObj.dic
		"""
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
				print "Failed: %s is empty." % self.url
				return -1
		self.update(dic)
		return dic

	def authors (self):
		"""
		x.authors()    -- list all authors in RedditObj
		"""
		return self.dic['articles'].keys()

	def ids (self, author):
		"""
		x.ids(author)    -- list all `article_id` of author in RedditObj
		"""
		return self.dic['articles'][author].keys()

	def keys (self):
		"""
		x.keys()    -- list all attributes(keys) in RedditObj.dic['artciles']
		"""
		return self.key_list

	def getitem (self, author, a_id, attr):
		"""
		x.getitem(author, a_id, attr)    -- return the value in RedditObj.dic['articles'][author][a_id][attr] 
		"""
		return self.dic['articles'][author][a_id][attr]

	def writeJSON (self, filename="reddit_user.json", dic={}):
		"""
		x.writeJSON(filename)    -- write RedditObj in the file
		"""
		self.dic['a_count'] = self.a_count
		self.dic['domain'] = self.domain
		self.dic['url'] = self.url
		self.dic['next_count'] = self.next_count
		self.dic['next_name'] = self.next_name
		self.dic['next_url'] = self.domain + self.user + "/submitted/.json?after=" + self.next_name
		if dic=={}:
			dic = self.dic
		with open(filename, 'w') as outfile:
			json.dump(dic, outfile, ensure_ascii=True)
		outfile.close()

	def readJSON (self, filename="reddit_user.json"):
		"""
		x.readJSON(filename)    -- read the file into RedditObj
		"""
		with open(filename, 'r') as infile:
			self.dic = json.loads(infile.read())
			self.domain = self.dic['domain']		 if self.dic.has_key('domain')	else None 
			self.a_count = self.dic['a_count']		 if self.dic.has_key('a_count') else None
			self.url = self.dic['url']				 if self.dic.has_key('url')		else None	
			self.next_count = self.dic['next_count'] if self.dic.has_key('next_count')	else None
			self.next_name = self.dic['next_name'] 	 if self.dic.has_key('next_name')	else None
			self.next_url = self.dic['next_url'] 	 if self.dic.has_key('next_url')	else None
		infile.close()
		return self.dic

	def update (self, new_dic):
		"""
		x.update(new_dic['articles'])    -- update this RedditObj articles information 
		                                     if new_dic = {'articles': 
		                                                       '$author1': { '$a_id11':..., '$a_id12':... },
		                                                       '$author2': {....}, ... 
		                                                  }                       
		"""
		if new_dic.has_key('articles') is True:
			print "Failed: new_dic should NOT have the key 'articles'."
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
	folder = 'data_new'
	filename = os.path.join(folder, "reddit_%s_%02d%02d.json" % (domain.split('/')[4], month, day))
	filename_sum = os.path.join(folder, "reddit_%s_sum.json" % (domain.split('/')[4]))

	if os.path.isdir(folder) is False:
		os.makedirs(folder)

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
		for user in article.authors():
			f.write("%s\n" % user)
			for a_id in article.ids(user):
				author = article.getitem(user, a_id, 'comments')
				f.write("%s\n" % author)
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
