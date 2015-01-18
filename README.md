# 팀 테헤란 슬리퍼즈: 큐리-크롤러(Curie-Crawler)
* * *

#### 1. 크롤러는 파일이 위치한 해당 디렉토리로 이동 후 아래와 같이 사용합니다.
```
$ python // move into the python shell
$ >> import curieCrawler
$ >> c = curieCrawler.Crawler([파일명]) // c = curieCrawler.Crawler("beat_tracks_info-4")
$ >> c.scrapFrom([소스명]) // c.scrapFrom("Youtube") "Youtube", "Melon", "Navermusic", "Bugs"
```

*위를 실행하게 되면 뒤에 소스명이 붙은 새로운 csv 파일이 생성되게 됩니다. (e.g. "beat_tracks_info-4(Melon)")*