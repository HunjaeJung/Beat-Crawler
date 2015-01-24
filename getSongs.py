# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import csv
import time

# 마지막일 것이라 추측: http://beatpacking.com/artists/100000000000000000000000062e09/
# int("62e09",16) = 405001
# 대략 40만개

# 16의 5승 (maximum)
limit = pow(16, 5)
Indexprefix = "000000"
base_url_artists = "http://beatpacking.com/artists/100000000000000000000000"

error_page = []
no_data_page = []

#total_machines_num = 8 # total number of machines
#this_machine_num = 1 # this machine number    
def start(total_machines_num, this_machine_num):
    # crawl machines 정보
    one_cycle = limit/total_machines_num        # one cycle range
    start_point = int(one_cycle*(this_machine_num-1))    # starting point
    end_point = int(one_cycle*this_machine_num)      # end point 

    # csv 파일명
    file_name = "beat_tracks_info"
    file_name = file_name + "-" + str(this_machine_num)      

    # 남은 시간 계산
    time_diff = 0   
    proc_before = 0
    proc_now = 0
    trackID_beat = 0

    with open("noDataPages","w") as clearfile:
        clearfile.write("")
    with open("errorPages","w") as clearfile:
        clearfile.write("")

    no_data_page_file = open("noDataPages", 'a')
    error_page_file = open("errorPages", 'a')

    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile, csv.excel)

        for i in range(start_point,end_point):
            IndexToHex = format(i, 'x')
            IndexToHexLength = len(IndexToHex)
            tempIndex = Indexprefix + IndexToHex
            Index = tempIndex[IndexToHexLength:]
            
            base_url = base_url_artists + Index

            if i != start_point:
                proc_now = time.time()
        
                if proc_now != proc_before:
                    time_diff = proc_now - proc_before
                    proc_before = proc_now

                total_time_left = time_diff * (end_point - i) # sec left
                min, sec = divmod(total_time_left,60)
                hour, min = divmod(min, 60)
                day, hour = divmod(hour, 24)
            	
                print ("%d일 %d시간 %d분 %d초 남았습니다." % (day, hour, min, sec))

            else:
            	proc_before = time.time()

            # 해당 URI가 404가 아닐때 가수명, 곡명, 사진을 가져옴
            try:
                soup = BeautifulSoup(urlopen(base_url).read())

                # 1. 앨범고르고
                select_albums = soup.select('body > div.container.outer > div')
                print("Artist %s has %d albums" % (Index, len(select_albums)))

                if len(select_albums) == 0:
                    no_data_page_file.write(Index)
                    no_data_page_file.write("\n")

                #2. 제목, 가수, 앨범, 썸네일유알엘, track_id of 비트, 출처 url_index
                for i in range(len(select_albums)):
                    album = select_albums[i].select('.title')[0].get_text().strip()
                    select_titles = select_albums[i].select('.track-list')
                    for j in range(len(select_titles)):
                        title = select_titles[j].select('.name')[0].get_text().strip()
                        artist = select_titles[j].select('.artist')[0].get_text().strip()
                        img_url = select_titles[j].select('.img-thumbnail')[0]['src']
                        trackID_beat = select_titles[j].select('.thumbnail')[0]['href']
                        trackID_beat = trackID_beat[(len(trackID_beat)-7):(len(trackID_beat)-1)]
                        row = [title, artist, album, img_url, trackID_beat, Index]
                        writer.writerow(row)
                    
            except IOError as e:
                error_page_file.write(Index)
                error_page_file.write("\n")
                print (e)
                continue

    error_page_file.close()
    no_data_page_file.close()

start(8,1)
