##### Tehran slippers team: Mobile music search engine (Crawler)
* * *

We, Tehran slippers, are making 'Mobile music search engine', and this code is for crawling **music infomation** and **track IDs**.

1. getBeatMusicinfo.py
	
    음악 정보(가수, 노래 제목, 앨범명, 앨범 이미지)를 가지고 있는 Beat에서 artist 번호를 기준으로 음악을 가져온다. 이때 Beat의 해당 음악 trackID도 함께 가져온다.

2. getTrackIDs.py

	비트를 제외한 음악 어플리케이션들의 trackID가 필요하다. 아래의 코드를 입력하면 해당 어플리케이션의 trackID를 받아와 새로운 csv를 만들고, Database에까지 밀어넣는다.

	```
    	import getTrackIDs
		c = Crawler("Music info filename.csv")
        c.scrapFrom("Music application")
```
	