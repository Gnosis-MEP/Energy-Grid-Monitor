#!/bin/bash
pipenv run python webserver/app.py &
echo 'webserver runnin'
cd src
sudo python3 cleanup_GPIO.py
sudo python3 monitor.py > out.log 2>&1 &
cd ../