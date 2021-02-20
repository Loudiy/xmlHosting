while true
do
	git pull
	python3 WebScrapper.py
	git pull
	git add xml/xmlIndex.xml
	git commit -m "Update catalog `date`"
	git push
done
