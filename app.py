# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
import csv
import time

reload(sys)
sys.setdefaultencoding('utf-8')

# akmu = "http://beatpacking.com/tracks/3000000000000000000000009ecd9c"
# errorUrl = "http://beatpacking.com/tracks/3000000000000000000000009ecd97"
# 0010a2에는 가수 이름이 없음. 그래서 중간에 오류남.

trackIdprefix = "000000"

# 16의 6승
limit = pow(16, 6)

# crawl machines information
total_machines_num = 8				# total number of machines
this_machine_num = 1				# this machine number
one_cycle = limit/total_machines_num		# one cycle range
start_point = one_cycle*(this_machine_num-1)	# starting point
end_point = one_cycle*this_machine_num		# end point

writable_artist = ""
writable_title = ""
writable_picture = ""

# csv 파일명
file_name = "beat_tracks_info"
file_name = file_name + "-" + str(this_machine_num)
csvFile = open(file_name, 'wb')
writer = csv.writer(csvFile, csv.excel)

# 남은 시간 계산
time_diff = 0	
proc_before = 0
proc_now = 0

for i in range(start_point,end_point):
	
    trackIdToHex = format(i, 'x')
    trackIdToHexLength = len(trackIdToHex)
    tempTrackId = trackIdprefix + trackIdToHex
    trackId = tempTrackId[trackIdToHexLength:]

    base_url = "http://beatpacking.com/tracks/300000000000000000000000" + trackId

    if i != start_point:
    	proc_now = time.time()

    	if proc_now != proc_before:
		time_diff = proc_now - proc_before
		proc_before = proc_now

	total_time_left = time_diff * (end_point - i) # sec left
	min, sec = divmod(total_time_left,60)
	hour, min = divmod(min, 60)
	day, hour = divmod(hour, 24)
	
	print "%d일 %d시간 %d분 %d초 남았습니다." % (day, hour, min, sec)
    else:
    	proc_before = time.time()

    # 해당 URI가 404가 아닐때 가수명, 곡명, 사진을 가져옴
    try:
        soup = BeautifulSoup(urlopen(base_url).read())
        artist = soup.select('.container > .thumbnail > .caption > .track-data > .artist')
        title = soup.select('.container > .thumbnail > .caption > .track-data > .track-name')
        picture = soup.select('.container > .thumbnail > .link > img')
	
    	if not artist: #artist is empty 
    		writable_artist="null"
    	else:
    		writable_artist = artist[0].get_text().strip()
    		
    	if not title: #title is empty 
    		writable_title="null"
    	else:
    		writable_title = title[0].get_text().strip()
    		writable_title = writable_title[:len(writable_title)-1]

    	if not picture: #picture is empty
    		writable_picture = "null"
    	else:
    		writable_picture = picture[0]['src'].strip()

        writer.writerow([writable_artist, writable_title, writable_picture, trackId])

        print "TrackId : %s Success" % trackId

    except IOError as e:
        print e
        continue



