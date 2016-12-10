#!/bin/bash

list=${1:-reddit_users.txt}
pattern=${2:-^}
title_ls=$(cat $list | grep $pattern)
time=$(date +%m%d)

folder=data
#output=${folder}/reddit_${user}_${time}.log

for user in $title_ls; do
	echo "Crawl: $user"
	python Reddit_user_crawler.py $user $folder #>> ${folder}/reddit_crawl_byUsers_${time}.log
done
