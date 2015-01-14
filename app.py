# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

# akmu = "http://beatpacking.com/tracks/3000000000000000000000009ecd9c"
# errorUrl = "http://beatpacking.com/tracks/3000000000000000000000009ecd97"

trackIdprefix = "000000"

# csv 파일명
file_name = "beat_tracks_info"
csvFile = open(file_name, 'wb')
writer = csv.writer(csvFile, csv.excel)

# 16의 6승
limit = pow(16, 6)
for i in range(limit):
    trackIdToHex = format(i, 'x')
    trackIdToHexLength = len(trackIdToHex)
    tempTrackId = trackIdprefix + trackIdToHex
    trackId = tempTrackId[trackIdToHexLength:]

    base_url = "http://beatpacking.com/tracks/300000000000000000000000" + trackId

    # 해당 URI가 404가 아닐때 가수명, 곡명, 사진을 가져옴
    try:
        soup = BeautifulSoup(urlopen(base_url).read())
        artist = soup.select('.container > .thumbnail > .caption > .track-data > .artist')
        title = soup.select('.container > .thumbnail > .caption > .track-data > .track-name')
        picture = soup.select('.container > .thumbnail > .link > img')
        writer.writerow([artist[0].get_text().strip(), title[0].get_text().strip(), picture[0]['src'].strip(), trackId])

        print "TrackId : %s Success" % trackId

    except IOError as e:
        print e
        continue



