#----- Protocol -----#

##### Beat #####
# 1.beat-ios: bpc://landing?type=play_radio&channel_id=60&track_id=300000000000000000000000{{musicId}} 
# - prefix: bpc://landing?type=play_radio&channel_id=60&track_id=300000000000000000000000
# - appendix: {{musicId}} 
# 2.beat-itunes: itms-apps://itunes.apple.com/app/beat-biteu-mulyo-ladio-sosyeol/id853073541?mt=8
# 3.beat-android: bpc://landing?type=play_radio&channel_id=60&track_id=300000000000000000000000{{musicId}} 
# - prefix: bpc://landing?type=play_radio&channel_id=60&track_id=300000000000000000000000
# - appendix: {{musicId}}
# 4.beat-googleplay: market://details?id=com.beatpacking.beat
##### End of Bugs #####

##### Bugs #####
# 1.bugs-ios: bugs3://app/tracks/3285722?autoplay=Y
# - prefix: bugs3://app/tracks/
# - appendix: 3285722?autoplay=Y
# 2.bugs-itunes: itms-apps://itunes.apple.com/kr/app//id348555322?mt=8 
# 3.bugs-android: 
# - prefix: bugs3://app/tracks/lists?title=&track_ids=
# - appendix: {{musicId}}&autoplay=Y
# 4.bugs-googleplay: market://details?id=com.neowiz.android.bugs
##### End of Bugs #####

##### Melon #####
# 1.melon-ios: meloniphone://play?ctype=1&menuid=29020101&cid=5536206
# - prefix: meloniphone://play?ctype=1&menuid=29020101&cid=
# - appendix: 5536206
# 2.melon-itunes: itms-apps://itunes.apple.com/kr/app/mellon-melon/id415597317?mt=8
# 3.melon-android: melonapp://play?ctype=1&menuid=29020101&cid=5536206
# - prefix: melonapp://play?ctype=1
# - appendix: &menuid=29020101&cid=5536206
# 4.melon-googleplay: market://details?id=com.iloen.melon
##### End of Melon #####

##### Navermusic #####
# 1.navermusic-ios: comnhncorpnavermusic://listen?version=3&trackIds=2037246
# - prefix: comnhncorpnavermusic://listen?version=3&trackIds=
# - appendix: 2037246
# 2.navermusic-itunes: itms-apps://itunes.apple.com/kr/app/id437760231
# 3.navermusic-android: intent://listen?version=3&trackIds=2037246#Intent;scheme=comnhncorpnavermusic;action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;package=com.nhn.android.music;end
# - prefix: intent://listen?version=3&trackIds=
# - appendix: 2037246#Intent;scheme=comnhncorpnavermusic;action=android.intent.action.VIEW;category=android.intent.category.BROWSABLE;package=com.nhn.android.music;end
# 4.navermusic-googleplay: market://details?id=com.nhn.android.music
##### End of Bugs #####

##### Youtube #####
# 1.youtube-ios: 
# - prefix: vnd.youtube://www.youtube.com/watch?v={{musicId}};feature=applinks
# - appendix: 
# 2.youtube-itunes: itms-apps://itunes.apple.com/app/youtube/id544007664?mt=8
# 3.youtube-android: http://www.youtube.com/watch?v={{musicId}};feature=applinks
# - prefix: http://www.youtube.com/watch?v=
# - appendix: {{musicId}};feature=applinks
# 4.youtube-googleplay: market://details?id=com.google.android.youtube
##### End of Bugs #####

#----- End of Protocol -----#

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

		
