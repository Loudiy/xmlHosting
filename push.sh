while true
do
	python3 WebScrapper.py
	git pull
	git add xml/xmlIndex.xml
	git commit -m "Update catalog"
	git push
done
