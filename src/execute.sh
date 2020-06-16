#!/bin/bash
sudo python3 cleanup_GPIO.py
sudo mv energenie.csv energenie.csv.old
sudo python3 monitor.py > out.log 2>&1 &
