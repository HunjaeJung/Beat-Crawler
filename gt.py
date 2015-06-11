# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import csv
import time

# update: 11 June 2015
# http://beatpacking.com/tracks/300000000000000000000000
# last: aa04af

# 16의 5승 (maximum)
def start(start, end):
    Indexprefix = "000000"
    base_url_track = "http://beatpacking.com/tracks/300000000000000000000000"

    start_point = int(start,16)
    end_point = int(end,16)

    # csv 파일명
    file_name = "beat_tracks_info_by_track"
    file_name = file_name + "-" + str(start) + "-" + str(end)

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

        for i in reversed(range(start_point,end_point)):
            IndexToHex = format(i, 'x')
            IndexToHexLength = len(IndexToHex)
            tempIndex = Indexprefix + IndexToHex
            Index = tempIndex[IndexToHexLength:]

            base_url = base_url_track + Index

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

            try:
                # 해당 URI가 404가 아닐때 가수명, 곡명, 사진을 가져옴
                soup = BeautifulSoup(urlopen(base_url).read())

                # 1. 앨범고르고
                select_track = soup.select('body > div.container.outer.track-card > div.container.comment > div')

                if len(select_track) == 0:
                    no_data_page_file.write(Index)
                    no_data_page_file.write("\n")

                else:
                    title =  select_track[0].select('.track-name')
                    if title:
                        title = title[0].get_text().strip().split(',')[0]
                    else:
                        continue

                    artist =  select_track[0].select('.artist')
                    if artist:
                        artist = artist[0].get_text().strip()
                    else:
                        artist = "null"

                    img_url =  select_track[0].select('.track-cover-img')
                    if img_url:
                        img_url = img_url[0]['src']
                    else:
                        img_url = "null"

                    album = "null"
                    trackID_beat = Index

                    print('We"ve got: ' + title + ' - ' + artist + ' for ' + trackID_beat)

                #2. 제목, 가수, 앨범, 썸네일유알엘, track_id of 비트, 출처 url_index
                row = [title, artist, album, img_url, trackID_beat, Index]
                writer.writerow(row)

            except IOError as e:
                error_page_file.write(Index)
                error_page_file.write("\n")
                print (e)
                continue


    error_page_file.close()
    no_data_page_file.close()

    return file_name
