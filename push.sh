#!/bin/bash

cd /home/nessreddine/Desktop/Nessreddine/xmlHosting

git pull
python3 WebScrapper.py
git pull
git add xml/xmlIndex.xml
git commit xml/xmlIndex.xml -m "Update catalog `date`"
date > LastModified.txt
git add LastModified.txt
git commit LastModified.txt -m "Update last time modified: `date`"
git push
./push.sh
