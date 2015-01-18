from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import sys
import csv
import time
import re

##### Protocol #####
### melon-ios: meloniphone://play?ctype=1&menuid=29020101&cid=5536206
# - prefix: meloniphone://play?ctype=1&menuid=29020101&cid=
# - appendix: 5536206
### melon-itunes: https://itunes.apple.com/kr/app/mellon-melon/id415597317?mt=8
### melon-android: melonapp://play?ctype=1&menuid=29020101&cid=5536206
# - prefix: melonapp://play?ctype=1
# - appendix: &menuid=29020101&cid=5536206
### melon-googleplay: market://details?id=com.iloen.melon
##### End of Protocol #####

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
	html_element = soup.select("#frm_defaultList > div > table > tbody > tr:nth-of-type(1) > td.t_left > div > div > button:nth-of-type(1)")
	if(len(html_element) == 0):
		print("music id is not in the html content")
	else: 
		music_id_list = re.findall(r"playSong\((.*)\)", str(html_element))[0].split(",")
		erase_quote = re.sub("'", "", music_id_list[0])
		music_id_list[0] = erase_quote
		final_music_id = "&menuid=" + music_id_list[0] + "&cid=" + music_id_list[1]
		print("this is music id", final_music_id)
		return final_music_id	
	
# scrapMelonMusicId("빅뱅 붉은노을");

