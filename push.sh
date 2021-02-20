while true
do
	git pull
	python3 WebScrapper.py
	git add xml/xmlIndex.xml
	git commit -m "Update catalog"
	git push
done
