import sys, os
from Reddit_crawler import RedditObj
from Reddit_crawler import RedditUser

if __name__ == '__main__':
	program		= sys.argv[0]
	user		= sys.argv[1]
	folder		= os.path.join(sys.argv[2], "user")
	# output		= os.path.join('data','reddit_UserSubmitted.json') 
	output		= os.path.join(folder,"reddit_%s.json" % user)
	if os.path.isdir(folder) is False:
		os.makedirs(folder)

	obj_old = RedditUser()

	print "User: %s" % user
	userobj = RedditUser(user)
	n_url = 0
	print userobj.url
	while n_url != -1:
		if userobj.url2json(userobj.next_url) == -1:
			print "User %s cannot find." % user
			break
		userobj.get_content(0,userobj.page_len)
		n_url = userobj.next_page()
		print n_url
	else:
		print "total: " + str(userobj.a_count)
	if os.path.exists (output) is True:
		obj_old.readJSON (output)
		obj_old.update (userobj.dic['articles'])
		userobj.dic['articles'] = obj_old.dic['articles']
	userobj.writeJSON (output)
