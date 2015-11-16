# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import csv
import time
import os
import datetime

# Get Music By Artist
# update: Aug 2015
# crawling URL: http://beatpacking.com/artists/100000000000000000000000063680/
# https://beatpacking.com/artists/10000000000000000000001b28ea3a/
# Last one: int("63680",16) = 407168
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Date		: 2015-11-16

Author		: Hunjae Jung
Description	:
    1. 수단과 방법을 가리지 않고, 딥링크 정보와 콘텐츠를 db에 indexing
    2. 계속해서 생성되는 최신 데이터들에 대한 indexing 자동화 기법 필요
    3. Crawling report 생성
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 16의 5승 (maximum)
def start(start, end):
    base_url_artists = "http://beatpacking.com/artists/1000000000000000000000"
    Indexprefix = "00000000"

    """""""""""""""""""""""""""""""""""""""""""""
    Convert hex string to decimal integer
    """""""""""""""""""""""""""""""""""""""""""""
    start_point = int(start,16)
    end_point = int(end,16)

    i = datetime.datetime.now()
    now_str = "{0}{1}{2}_{3}-{4}".format(str(i.year)[2:], str(i.month), str(i.day), start, end)

    # csv 파일명
    appendix = str(start) + "-" + str(end)

    file_name = "./data/"+now_str+"/crawled/artist-" +appendix+".csv"
    no_data_file_name = "./data/"+now_str+"/no_data/404-" +appendix+".csv"
    error_file_name = "./data/"+now_str+"/error/error-" +appendix+".csv"

    # 남은 시간 계산
    time_diff = 0
    proc_before = 0
    proc_now = 0
    track_addr = 0

    """""""""""""""""""""""""""""""""""""""""""""
    Create date directories if there is no exists
    """""""""""""""""""""""""""""""""""""""""""""
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    os.makedirs(os.path.dirname(no_data_file_name), exist_ok=True)
    os.makedirs(os.path.dirname(error_file_name), exist_ok=True)

    no_data_page_file = open(no_data_file_name, 'a')
    error_page_file = open(error_file_name, 'a')

    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile, csv.excel)
        row = ["title", "artist", "album", "img_url", "track_addr", "Index"]
        writer.writerow(row)

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
                        if select_titles[j].select('.name')[0]:
                            title = select_titles[j].select('.name')[0].get_text().strip()
                        else:
                            title = ""
                        if select_titles[j].select('.artist')[0]:
                            artist = select_titles[j].select('.artist')[0].get_text().strip()
                        else:
                            artist = ""
                        if select_titles[j].select('.img-thumbnail')[0]:
                            img_url = select_titles[j].select('.img-thumbnail')[0]['src']
                        else:
                            img_url = ""
                        if select_titles[j].select('.thumbnail')[0]:
                            #track_addr = select_titles[j].select('.thumbnail')[0]['href'].split("tracks/")[1]
                            track_addr = select_titles[j].select('.thumbnail')[0]['href']
                        else:
                            track_addr = ""

                        row = [title, artist, album, img_url, track_addr, Index]
                        writer.writerow(row)

            except IOError as e:
                error_page_file.write(Index)
                error_page_file.write("\n")
                print (e)
                continue

    error_page_file.close()
    no_data_page_file.close()

    return file_name

if __name__ == "__main__":
    start(sys.argv[1], sys.argv[2])
