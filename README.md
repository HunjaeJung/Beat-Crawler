##### 프로그램 설명

비트앱의 트랙 정보를 가져올 수 있는 크롤러 코드입니다. 크롤러는 run.sh 소스코드 내 지정된 파라미터에 맞춰(start, end) 순차적으로 돌아가며, artist id와 track id 두 가지 기준을 활용하여 돌릴 수 있습니다.

artist id 기준(gmba.py)의 경우, 한 페이지에 곡 정보가 다량으로 들어가 있기 때문에 매우 빠르게 돌릴 수 있는 반면, track id 기준(gmbt.py)의 경우 중간중간 빠지는 곡 없이 모든 곡을 크롤링 할 수 있습니다.

### 폴더 구조 및 파일 정보

1. run.sh: tmux을 사용하여 자동으로 멀티 프로세싱을 하게 만듭니다. 소스코드 상단의 변수들을 바꾸어, 창을 얼마나 띄울지, 어디서부터 어디까지 긁어올지 등을 정할 수 있습니다.
2. gmba.py: get music by artist id의 줄인 말로, artist id를 기준으로 음악 정보들을 크롤링해옵니다.
3. gmbt.py: get music by track id의 줄임 말로, track id를 기준으로 음악 정보들을 크롤링해옵니다.
4. data: 크롤링한 데이터 결과값들이 들어갑니다.
 1. data/crawled: 최종 크롤링된 음악정보들 파일들이 저장된다.
 2. data/error: error message를 주는 id를 저장한다.
 3. data/no_data: 가긴 갔는데 data가 없는 id를 저장한다.
5. temp: 현재는 사용되지 않는 소스들입니다.
