# import for Youtube
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import re

f = open("token.txt", 'r') 
token = f.readline() 
f.close()

DEVELOPER_KEY = token	
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def scrapYoutubeMusicId(original_artist, original_title, maxResults):
	original_query = original_artist + original_title
	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
		q=original_query,
		part="id,snippet",
		maxResults=maxResults
	).execute()

	videos = []

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			video = {
				"title": search_result["snippet"]["title"],
				"id": search_result["id"]["videoId"] 			
			}
			videos.append(video)
	
	result = re.findall(original_artist + r"+", videos[0]["title"]) 
	if(len(result) == 0):
		print("no result")
		return "0"
	else:
		print("no result")
		return videos[0]["id"]

scrapYoutubeMusicId("빅뱅", "붉은노을", 1)