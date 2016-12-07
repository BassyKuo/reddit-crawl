#!/bin/bash

list=${1:-reddit_users.txt}
#pages=${2:-1000}
title_ls=$(cat $list)
time=$(date +%m%d)

output=data/reddit_${domain}_${time}.log

for user in $title_ls; do
	#echo "Crawl: $domain"	
	#echo "pages: $pages"
	python crawl_user_submit.py $user #>> data/reddit_crawl_byUsers.log
done


