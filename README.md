# 팀 테헤란 슬리퍼즈: 큐리-크롤러(Curie-Crawler)
* * *

#### 1. 우선 적으로 음원정(제목, 가수, 앨범, 앨범이미지 url 등)을 받아오기 위해, 아래와 같은 코드로 크롤링을 실시합니다. (이 코드는 Beats를 바탕으로 정보를 수집합니다.)
```
$ python3
>> import getSongs
>> getSongs.start(돌릴 머신 개수, 현재 머신 번호) // getSongs.start(8,1)
```

* 돌릴 머신 개수는 2,4,8 등의 숫자(2^n)로 사용
* errorPages는 HTTP 404 에러
* noDataPages는 페이지는 있지만, 데이터가 없는 경우 (재 크롤링 우선순위)

#### 2. 음원정보를 받아온 뒤, 크롤러는 파일이 위치한 해당 디렉토리로 이동 후 아래와 같이 사용합니다.
```
$ python3 // move into the python shell
$ >> import curieCrawler
$ >> c = curieCrawler.Crawler([파일명]) // c = curieCrawler.Crawler("beat_tracks_info-4")
$ >> c.scrapFrom([소스명]) // c.scrapFrom("Youtube") "Youtube", "Melon", "Navermusic", "Bugs"
```

*위를 실행하게 되면 뒤에 소스명이 붙은 새로운 csv 파일이 생성되게 됩니다. (e.g. "beat_tracks_info-4(Melon)")*

#### 3. 1번과 2번의 과정을 한번의 코드로 실행시키기 위해 startToCrawl.py를 수정한 뒤 아래와 같이 입력합니다.
```
$ python3 startToCrawl.py
```