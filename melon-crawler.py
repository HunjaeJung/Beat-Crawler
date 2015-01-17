from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import sys
import csv
import time
import re

def scrapMelonMusicId(original_query):
	# encode original_query into modified_query
	modified_query = quote(original_query)
	modified_url = "http://www.melon.com/search/song/index.htm?q=" + modified_query + "&section=&searchGnbYn=Y&ipath=srch_form"

	# opener = urllib.request.build_opener()
	# opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	# opener.open('http://www.example.com/')
	f = urlopen(modified_url)
	html = f.read().decode('utf-8')
	soup = BeautifulSoup(html)
	html_element = soup.select("#frm_defaultList > div > table > tbody > tr:nth-of-type(1) > td > div > input")
	music_id_list = re.findall(r'value="(.*)"\s?', str(html_element))
	if(len(music_id_list) == 0):
		print("music id not in the html content")
	else:
		print("found music id")
		music_id = music_id_list[0]
		return music_id		
	
# scrapMelonMusicId("빅뱅 붉은 노을");


