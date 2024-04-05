all :
	python3.11 bot.py

install-reqs :
	pip install -r requirements.txt

clear-db :
	python3.11 bin/clear-db.py