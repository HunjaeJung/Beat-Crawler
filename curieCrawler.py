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

class Crawler():
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

	def scrapMelon(self, title, artist):
		try:
			originalQuery = artist + " " + title
			# encode originalQuery into modifiedQuery
			modifiedQuery = quote(originalQuery)
			modifiedURL = "http://www.melon.com/search/song/index.htm?q=" + modifiedQuery + "&section=&searchGnbYn=Y&ipath=srch_form"

			f = urlopen(modifiedURL)
			html = f.read().decode('utf-8')
			soup = BeautifulSoup(html)
			htmlElement = soup.select("#frm_defaultList > div > table > tbody > tr:nth-of-type(1) > td.t_left > div > div > button:nth-of-type(1)")
			if(len(htmlElement) == 0):
				print("music id is not in the html content")
				return "0"
			else: 
				musicIdList = re.findall(r"playSong\((.*)\)", str(htmlElement))[0].split(",")
				# eraseQuote = re.sub("'", "", musicIdList[0])
				# musicIdList[0] = eraseQuote
				# finalMusicId = "&menuid=" + musicIdList[0] + "&cid=" + musicIdList[1]
				print("music id is found and it is ", musicIdList[1])
				return musicIdList[1]
		
		except Exception as e: 
			print("error from scrapMelon method: ", e)

	def scrapYoutube(self, title, artist):
		try:
			originalQuery = artist + " " + title
			
			youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, developerKey=self.DEVELOPER_KEY)

			searchResponse = youtube.search().list(
				q=originalQuery,
				part="id,snippet",
				maxResults=1
			).execute()

			videos = []

			for searchResult in searchResponse.get("items", []):
				if searchResult["id"]["kind"] == "youtube#video":
					video = {
						"title": searchResult["snippet"]["title"],
						"id": searchResult["id"]["videoId"] 			
					}
					videos.append(video)
			
			matchResult = re.match(r"(" + re.escape(artist) + r")?[-\s@]*(" + re.escape(title) + r")?", videos[0]["title"])
			
			if(matchResult.group(1,2)[0] != None and matchResult.group(1,2)[1] != None):
				print("two matches found from regex findall", matchResult.group(1,2))
				return videos[0]["id"]
			else:
				print("at least one no match found from regex findall")
				return "0"

		except Exception as e:
			print("error from scrapYoutube: ", e)

	def scrapNavermusic(self, title, artist):
		try:
			modifiedURL = "http://music.naver.com/search/search.nhn?query=" + quote(title) 
			if artist != "null":
				modifiedURL = modifiedURL + "%20" + quote(artist)

			# url open, html read and beautifulsoup
			a=urlopen(modifiedURL).read()
			soup = BeautifulSoup(urlopen(modifiedURL).read())
			
			# get play button by class name
			playButton = soup.findAll('a', { "class" : "_play_ico" })

			# if there is no music, return
			if not playButton:
				print("no match found from Navermusic")
				return "0"
			else:
				trackId = playButton[0]['class'][2].split(',')[2].split(':')[1]
				print("music id is found and it is ", trackId)
				return trackId

		except Exception as e:
			print("error from scrapNavermusic: ", e)

	def scrapBugs(self, title, artist):
		try:
			modifiedURL = "http://search.bugs.co.kr/track?q=" + quote(title) 
			if artist != "null":
				modifiedURL = modifiedURL + "%20" + quote(artist)

			# url open, html read and beautifulsoup
			a=urlopen(modifiedURL).read()
			soup = BeautifulSoup(urlopen(modifiedURL).read())
			
			# get play button by class name
			playButton = soup.findAll('a', { "class" : "btnPlay" })

			# if there is no music, return
			if not playButton:
				print("no match found from Bugs")
				return "0"
			else:
				trackId = playButton[0]['onclick'].split('\'')[1]
				print("music id is found and it is ", trackId)
				return trackId

		except Exception as e:
			print("error from scrapBugs: ", e)

	
	def scrapSource(self, source, title, artist):
		if source == "Melon":
			musicId = self.scrapMelon(title, artist)
			return musicId
		elif source == "Youtube":
			musicId = self.scrapYoutube(title, artist)
			return musicId
		elif source == "Navermusic":
			musicId = self.scrapNavermusic(title, artist)
			return musicId
		elif source == "Bugs":
			musicId = self.scrapBugs(title, artist)
			return musicId

	# Either from "Melon", "Youtube", "Navermusic", "Bugs"
	def scrapFrom(self, source):
		try:
			with open(self.fileName, mode='r', newline='') as f:
				reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)

				with open(self.fileName + '(' + source + ')','w') as csvFile:
					writer = csv.writer(csvFile, csv.excel)

					for row in reader:
						artist = row[0] 
						title = row[1]
						trackId = self.scrapSource(source, title, artist)
						row.append(trackId)
						writer.writerow(row)		
		
		except Exception as e:
			print("error from createCSV method: ", e)

		
