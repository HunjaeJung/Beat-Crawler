#!/bin/bash

### bash run.sh
### Beat 크롤링 프로그램을 Autorun 합니다. 자동으로 verticalN*2등분하여 tmux를 split하고, 크롤링을 시작합니다.
verticalN=5
#crawlBy="artist"
crawlBy="track"
#start=$1
#end=$2
#start="0"
#end="70000"
start="0"
end="aa1000"

if [ $crawlBy == "artist" ]
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
###vertically, resulting in eight seperate panes
for ((i=1;i<$((verticalN*2));i=i+2))
do
	tmux select-pane -t $i
	tmux split-window -h
done

# hex to dec
h2d(){
    echo "ibase=16; $@"|bc
}
# dec to hex
d2h(){
    echo "obase=16; $@"|bc
}

# convert hexadecimal to decimal
jump=$(((16#$end-16#$start)/10))
next=$((start+jump))
tmux send-keys -t 1 "clear" C-m

for ((i=1;i<$((verticalN*2));i++))
do
	tmux select-pane -t $i
	# convert decimal to hexadecimal
    start16=$(d2h $start)
    next16=$(d2h $next)
	tmux send-keys -t $i "$file $start16 $next16" C-m
	start=$((start+jump))
	next=$((start+jump))
	sleep 0.5
done

lastPane=$((verticalN*2))
tmux select-pane -t $lastPane
# convert decimal to hexadecimal (end is already hexadecimal)
start16=$(d2h $start)
tmux send-keys -t $lastPane "$file $start16 $end" C-m
