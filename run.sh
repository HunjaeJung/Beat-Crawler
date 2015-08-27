#!/bin/bash

### sh autorun.sh 0 600000
### Beat 크롤링 프로그램을 Autorun 합니다. 자동으로 n등분하여 tmux를 split하고, 크롤링을 시작합니다.
verticalN=5
crawlBy="artist"
#crawlBy="track"

if crawlBy="artist"
then
	file="python3 gmba.py"
else
	file="python3 gmbt.py"
fi

cmt="This Crawler is going to crawl beat tracks by using"
echo $cmt$crawlBy

###this is going to split the pane into four 
###even horizontal panes
for ((i=1;i<$verticalN;i++)) do
	tmux split-window -v
	tmux select-pane -t $i
done

tmux send-keys -t 1 "clear" C-m
tmux select-layout even-vertical

###this will split each of the four panes
###vertically, resulting in eight seperate 
###panes
for ((i=1;i<$((verticalN*2));i=i+2))
do
	tmux select-pane -t $i
	tmux split-window -h
done

start=$1
end=$2

start="0"
end="70000"

jump=$(((end-start)/10))
next=$((start+jump))
tmux send-keys -t 1 "clear" C-m

for ((i=1;i<$((verticalN*2));i++))
do
	tmux select-pane -t $i
	tmux send-keys -t $i "$file $start $next" C-m
	start=$((start+jump))
	next=$((start+jump))
	sleep 0.5
done

lastPane=$((verticalN*2))
tmux select-pane -t $lastPane
tmux send-keys -t $lastPane "$file $start $end" C-m
