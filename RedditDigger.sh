#!/bin/bash

list=${1:-reddit_subtitle.txt}
title_ls=$(cat $list)
time=$(date +%m%d)

output=data/reddit_${domain}_${time}.log

for domain in $title_ls; do
	echo "Crawl: $domain"	
	python crawl.py https://www.reddit.com/r/${domain}/
	echo ""
done

sort reddit_users.txt | uniq > reddit_users_${time}.txt
