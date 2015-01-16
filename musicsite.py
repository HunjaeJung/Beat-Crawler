# -*- coding:utf-8 -*-
# python v3.4

# title: music info crawler (navermusic)
# 1. /data/csv 를 읽는다.
# 2. 가수와 제목을 받아온다. artist, title
# 3. 제목 기준으로 쿼리를 때리고, 가수로 한번 더 필터링한다.
# 4. 가수가 null인 경우는 제목만

from bs4 import BeautifulSoup
from urllib.request import urlopen, build_opener
from urllib.parse import quote
import csv
import sys
import time

file_name = "./" 

# navermusic or bugs
site_name = ["navermusic", "bugs"]

site_url = {"navermusic": "http://music.naver.com/search/search.nhn?query=", \
		"bugs": "http://search.bugs.co.kr/track?q="}

site_class = {"navermusic": "_play_ico", \
		"bugs": "btnPlay"}

def crawling_in(sitename, title, artist):
	title = quote(title)
	artist = quote(artist) #encodeURI (Korean -> %encode)

	try:
		# compelete url
		url_with_query = site_url[sitename] + title 
		if artist != "null":
			url_with_query = url_with_query + "%20" + artist
			print(url_with_query)

		# url open, html read and beautifulsoup
		a=urlopen(url_with_query).read()
		soup = BeautifulSoup(urlopen(url_with_query).read())
		
		# get play button by class name
		play_btn = soup.findAll('a', site_class[sitename])

		# if there is no music, return
		if not play_btn:
			print("There is no music matched")
			return 0

		# get track id
		if sitename == "navermusic":
			trackid = play_btn[0]['class'][2].split(',')[2].split(':')[1] # only for navermusic
		else:
			trackid = play_btn[0]['onclick'].split('\'')[1] # only for bugs

		return trackid

	except IOError as e:
		return

if __name__ == '__main__':
	# beat data file open
	with open(file_name, mode='r+', newline='') as f:
		
		for i in range(len(site_name)):
			reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)

			# write file open (append new trackid)
			with open(file_name+"-"+site_name[i],'w') as csvFile:
				writer = csv.writer(csvFile, csv.excel)

				# one by one row
				for row in reader:
					artist = row[0]; title = row[1]
					trackid = crawling_in(site_name[i], title, artist)
					row.append(trackid)
					writer.writerow(row)
			f.seek(0)
