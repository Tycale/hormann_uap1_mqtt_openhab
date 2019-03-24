for i in 21 22 23 24 25; do gpio mode $i OUT; done
for i in 21 22 23 24 25; do gpio write $i 1; done
