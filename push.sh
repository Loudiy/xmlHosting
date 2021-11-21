#!/bin/bash

cd /home/nessreddine/Desktop/Nessreddine/xmlHosting

git pull
python3 WebScrapper.py
git pull
git add xml/xmlIndex.xml
git commit -m "Update catalog `date`"
date > LastModified.txt
"Nessredddine" > test.txt
git add LastModified.txt
git commit -m "Update last time modified"
git push
./push.sh
