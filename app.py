# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

artistList = []
titleList = []
trackIdList = []
pictureList = []

# akmu = "http://beatpacking.com/tracks/3000000000000000000000009ecd9c"
# errorUrl = "http://beatpacking.com/tracks/3000000000000000000000009ecd97"

# 16의 6승
limit = pow(16, 6)
for i in range(limit):
    trackId = format(limit, 'x')
    base_url = "http://beatpacking.com/tracks/300000000000000000000000" + trackId

    # 해당 URI가 404가 아닐때 가수명, 곡명, 사진을 가져옴
    try:
        soup = BeautifulSoup(urlopen(base_url).read())
        artists = soup.select('.container > .thumbnail > .caption > .track-data > .artist')
        for artist in artists:
            artistList.append(artist.get_text().strip())

        titles = soup.select('.container > .thumbnail > .caption > .track-data > .track-name')
        for title in titles:
            titleList.append(title.get_text().strip())

        pictures = soup.select('.container > .thumbnail > .link > img')
        for picture in pictures:
            pictureList.append(picture['src'].strip())

        trackIdList.append(trackId)

    except IOError:
        continue

# 저장한 가수명의 수만큼 반복문을 돌리기 위한 변수
searchedItemlen = len(artistList)

# csv 파일명
file_name = "beat_tracks_info"

with open(file_name, 'wb') as f:
    writer = csv.writer(f, csv.excel)
    for k in range(searchedItemlen):
        writer.writerow([artistList[k], titleList[k], pictureList[k], trackIdList[k]])