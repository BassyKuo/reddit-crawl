#!/bin/bash

list=${1:-reddit_subtitle.txt}
title_ls=$(cat $list)
time=$(date +%m%d)

folder=data
output=${folder}/reddit_${domain}_${time}.log

for domain in $title_ls; do
	echo "Crawl: $domain"	
	python Reddit_crawler.py https://www.reddit.com/r/${domain}/ $folder
	echo ""
done

sort reddit_users.txt | uniq > reddit_users_${time}.txt
