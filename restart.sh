#!/bin/bash
while true; do
   su - pi -c 'cd /home/pi/baroness && FRAMEBUFFER=/dev/fb1 startx ./run.py > baroness.out'
   now=$(date)
   echo "Current time : $now" >> restart.log
   killall pigpiod
   sleep 5
   pigpiod
   sleep 5
done
