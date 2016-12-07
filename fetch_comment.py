import json
import urllib2
import os, sys

def url2json (url):
	"""
	content = url2json('http://www.reddit.com/r/subreddit/comments/a_id/.json')    -- return json_content
	"""
	if ('.json' in url) is False:
		url = url + '.json'
	request = urllib2.Request(url)
	request.add_header ("User-Agent",
						"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
	respond = urllib2.urlopen(request)
	content = json.loads(respond.read())
	return content

def fetch_comment (comment, dic, level, num):
	"""
	comment = fetch_comment({}, content[1], 1, 0)    -- return comment part in the json_content

	comment = {
		"$c_name_1" : { 'level' , 'parent_id' , 'body' , ... },
		"$c_name_2" : { 'level' , 'parent_id' , 'body' , ... },
		....
	}
	"""
	c_name = dic['data']['children'][num]['data']['name']
	comment[c_name] = {}
	comment[c_name]['child_id'] = {}
	comment[c_name]['level'] = level
	# print c_name
	# print dic['data']['children'][num]['data'].keys()
	for item in dic['data']['children'][num]['data'].keys():
		if item != 'replies':
			comment[c_name][item] = dic['data']['children'][num]['data'][item]
	# for item in comment[c_name].keys():
		# print "\t%s:\t%s" % (item, comment[c_name][item])
	if dic['data']['children'][num]['data']['replies'] != '':
		comment[c_name]['child_id'] = {
			dic['data']['children'][num]['data']['replies']['data']['children'][i]['data']['name']:'' 
			for i in range(0,len(dic['data']['children'][num]['data']['replies']['data']['children']))
			}
		comment.update(fetch_comment(comment, dic['data']['children'][num]['data']['replies'], level+1, 0))
	if num+1 < len(dic['data']['children']):
		comment.update(fetch_comment(comment, dic, level, num+1))
	return comment


if __name__ == '__main__':
	program = sys.argv[0]
	# url		= sys.argv[1]
	url = "https://www.reddit.com/r/AskReddit/comments/4ue58r/what_illustrates_that_political_correctness_has/.json"
	c = url2json (url)
	comment = {}
	comment = fetch_comment (comment, c[1], 1, 0)
	for c_name in comment.keys():
		print c_name
		for item in comment[c_name].keys():
			print "\t%s:\t%s" % (item, comment[c_name][item])
