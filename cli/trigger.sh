i=$1
gpio write $i 1
gpio write $i 0
sleep 0.5
gpio write $i 1
