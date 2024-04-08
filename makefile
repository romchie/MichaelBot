CLEAR_TYPE ?= all
NOTIFY ?= True

all :
	python3.11 bot.py ${NOTIFY}

install-reqs :
	pip install -r requirements.txt

clear-db :
	python3.11 bin/clear-db.py ${CLEAR_TYPE}