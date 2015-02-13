##### Youtube #####
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

##### Beautiful Soup #####
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote

##### Common #####
import sys
import csv
import time
import re
import logging
import datetime
import pymysql

class database:
	def __init__(self):
		return

	def connectDB(self):
		# self.conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='curie_finish', charset='utf8')
		self.conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='xpgpfks!@', db='curie_finish', charset='utf8')
		self.cur = self.conn.cursor()
		return

	def createTables(self):
		return

	def InsertAppInfo(self):
		# self.cur.execute("select * from app_info")
		# for res in self.cur:
		# 	print(res)
		return

	def InsertSongInfo(self, title, artist, album, ImgURL, lyrics):

		return

	def InsertLinkIds(self, title, artist, album, appTrackID, appnum):
		# query go!
		try:
			prev = time.time()
			query_list = []
			query_list.append('INSERT INTO link_ids(`song_id`, `app_id`, `link_id`, `usable`) VALUES((SELECT id FROM curie_finish.song_info WHERE title=')
			query_list.append('"')
			query_list.append(title)
			query_list.append('"')
			query_list.append(' AND artist = ')
			query_list.append('"')
			query_list.append(artist)
			query_list.append('"')
			query_list.append(' AND album = ' )
			query_list.append('"')
			query_list.append(album)
			query_list.append('"')
			query_list.append(' limit 1), ')
			query_list.append(str(appnum))
			query_list.append(', ')
			query_list.append('"')
			query_list.append(appTrackID)
			query_list.append('"')
			query_list.append(', True)')
			query = ''.join(query_list)

			self.cur.execute(query)
			self.conn.commit()
			after = time.time()
			print(query)
			print("Insert row takes" + str(round(after-prev, 10)) + " sec")

		except Exception as e:
			logging.exception(e)
			return

class Crawler(database):
	def __init__(self, fileName):
		self.fileName = fileName
		
		# load token from token.txt for Youtube scrapping
		f = open("token.txt", 'r') 
		token = f.readline() 
		f.close()

		self.DEVELOPER_KEY = token	
		self.YOUTUBE_API_SERVICE_NAME = "youtube"
		self.YOUTUBE_API_VERSION = "v3"

	def changeFile(self, fileName):
		self.fileName = fileName

	def scrapMelon(self, title, artist, album):
		try:
			originalQuery = artist + " " + title + " " + album
			# encode originalQuery into modifiedQuery
			modifiedQuery = quote(originalQuery)
			modifiedURL = "http://www.melon.com/search/song/index.htm?q=" + modifiedQuery + "&section=&searchGnbYn=Y&ipath=srch_form"

			f = urlopen(modifiedURL, timeout=5)
			html = f.read().decode('utf-8')
			soup = BeautifulSoup(html)
			htmlElement = soup.select("#frm_defaultList > div > table > tbody > tr:nth-of-type(1) > td.t_left > div > div > button:nth-of-type(1)")
			if(len(htmlElement) == 0):
				print("[Melon] id is not in the html content")
				return "0"
			else: 
				musicIdList = re.findall(r"playSong\((.*)\)", str(htmlElement))[0].split(",")
				print("[Melon] id is found and it is ", musicIdList[1])
				return musicIdList[1]
		
		except: 
		   	logging.exception('Got exception on scrapMelon: ' + artist + '-' + title)
		   	return "0"

	def scrapYoutube(self, title, artist):
		try:
			originalQuery = artist + " " + title

			# encode originalQuery into modifiedQuery
			modifiedQuery = quote(originalQuery)
			modifiedURL = "https://www.youtube.com/results?search_query=" + modifiedQuery

			print(modifiedURL)
			f = urlopen(modifiedURL, timeout=5)
			html = f.read().decode('utf-8')
			soup = BeautifulSoup(html)
			NumOfResults = soup.select("#content > div > div > div > div.branded-page-v2-primary-col > div > div.branded-page-v2-body.branded-page-v2-primary-column-content > div.search-header.yt-uix-expander.yt-uix-expander-collapsed > div.filter-top > div > p > strong")
			if NumOfResults[0].get_text().strip() == "0":
				print("[Youtube] id is not in the html content")
				return "0"

			htmlElement = soup.select("#section-list > li > ol > li > div > div > div.yt-lockup-content > h3 > a")

			found = 0
			for i in range(len(htmlElement)):
				html = htmlElement[i].get_text().strip()
				if title in html:
					found=1
					break
				else:
					continue

			if(found == 0):
				print("[Youtube] id is not in the html content")
				return "0"
			else: 
				musicIdList = htmlElement[i]['href'].split('=')[1]
				musicIdList = musicIdList.split('&')[0]
				print("[Youtube] id is found and it is ", musicIdList)
				return musicIdList

		except:
		   	logging.exception('Got exception on scrapYoutube: ' + artist + '-' + title)
		   	return "0"

	def scrapNavermusic(self, title, artist, album):
		try:
			modifiedURL = "http://music.naver.com/search/search.nhn?query=" + quote(title) 
			if artist != "":
				modifiedURL = modifiedURL + "%20" + quote(artist)
			if album != "":
				modifiedURL = modifiedURL + "%20" + quote(album)

			# url open, html read and beautifulsoup
			contents=urlopen(modifiedURL, timeout=5)
			soup = BeautifulSoup(contents.read())
			
			# get play button by class name
			playButton = soup.findAll('a', { "class" : "_play_ico" })

			# if there is no music, return
			if not playButton:
				print("[Navermusic] id is not in the html content")
				return "0"
			else:
				trackId = playButton[0]['class'][2].split(',')[2].split(':')[1]
				print("[Navermusic] id is found and it is ", trackId)
				return trackId

		except:
		   	logging.exception('Got exception on scrapNavermusic: ' + artist + '-' + title)
		   	return "0"

	def scrapBugs(self, title, artist, album):
		try:
			modifiedURL = "http://music.bugs.co.kr/player/track/ajax/search?keyword=" + quote(title) 
			if artist != "":
				modifiedURL = modifiedURL + "%20" + quote(artist)
			modifiedURL = modifiedURL + "&page=1&decorator='blank_rest'&isBasic='N'"

			print(modifiedURL)
			# url open, html read and beautifulsoup
			contents=urlopen(modifiedURL, timeout=5)
			soup = BeautifulSoup(contents.read())
			
			# get play button by class name
			playButton = soup.select("#scrollSearch > ul > li")

			print(playButton[0]['id'])
			print("--------")
			# if there is no music, return
			if not playButton:
				print("[Bugs] id is not in the html content")
				return "0"
			else:
				trackId = playButton[0]['id']
				print("[Bugs] id is found and it is ", trackId)
				return trackId

		except:
		   	logging.exception('Got exception on scrapBugs: ' + artist + '-' + title)
		   	return "0"
	
	def scrapSource(self, source, title, artist, album):
		if source == "Melon":
			musicId = self.scrapMelon(title, artist, album)
			return musicId
		elif source == "Youtube":
			musicId = self.scrapYoutube(title, artist)
			return musicId
		elif source == "Navermusic":
			musicId = self.scrapNavermusic(title, artist, album)
			return musicId
		elif source == "Bugs":
			musicId = self.scrapBugs(title, artist, album)
			return musicId

	def scrapFrom(self, source, appID):
		try:
			LOG_FILENAME = 'logging.out-' + source
			logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
			logging.debug('Musicurie traceback log. It starts at')
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			logging.debug(st)
			
			self.connectDB()

			with open(self.fileName, mode='r', newline='') as f:
				# connect to database
				reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

				new_filename = self.fileName + '(' + source + ')'
				with open(new_filename,'w') as csvFile:
					writer = csv.writer(csvFile, csv.excel)

					# [Artist], [Title], [Album], [AlbumImageUrl], [BeatArtistID], [BeatTrackID]
					for row in reader:
						title = row[0]
						artist = row[1] 
						album = row[2]
						
						prev = time.time()
						trackId = self.scrapSource(source, title, artist, album)
						after = time.time()
						print(str(round(after-prev, 2)) + " sec for " + source)

						if not trackId:
							trackId=0
						row.append(trackId)

						writer.writerow(row)	

						# print(title)
						# print(artist)
						# print(trackId)
						if trackId != "0":
							self.InsertLinkIds(title, artist, album, trackId, appID)
				return new_filename

		except:
		   logging.exception('Got exception on scrapAll')

c = Crawler("./data/beat_tracks_info-3")
c.scrapFrom("Melon",3)
