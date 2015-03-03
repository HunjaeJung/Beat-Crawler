##### Tehran slippers team: Mobile music search engine (Crawler)
* * *

We, Tehran slippers, are making 'Mobile music search engine', and this code is for crawling **music infomation** and **track IDs**.

1. getBeatMusicinfo.py
	
    음악 정보(가수, 노래 제목, 앨범명, 앨범 이미지)를 가지고 있는 Beat에서 artist 번호를 기준으로 음악을 가져온다. 이때 Beat의 해당 음악 trackID도 함께 가져온다. start 함수 하나만 존재하는데, 넓은 범위를 여러개의 크롤링 머신을 나눠 돌리기 위해 입력값으로는 시작값, 종료값, 그리고 머신번호가 들어간다. 
	
	* 사용 방법

    ```
	import getBeatMusicInfo
    getBeatMusicInfo.start("1", "ffffff", 1) # start, end, machine number
    ```

2. getTrackIDs.py

	비트를 제외한 음악 어플리케이션들의 trackID가 필요하다. 아래의 코드를 입력하면 해당 어플리케이션의 trackID를 받아와, Database에 까지 밀어넣는다. 효율적인 크롤링을 위해 멀티프로세싱을 지원하며, ./data 폴더내에 파일들을 기준(제목, 가수, 앨범명)으로 크롤링을 실시한다.

	* 사용 방법
	
	```
    python3 getTrackIDs.py
	```
	