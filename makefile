# CLEAR_TYPE ?= all
# NOTIFY ?= True

all :
	python3.11 bot.py

# start the bot with a notification
notify : 
	python3.11 bot.py notify

sync :
	python3.11 bot.py sync

install-reqs :
	pip install -r requirements.txt

clear-db :
	python3.11 utils/clear-db.py

add-item :
	python3.11 bin/box_data/add-box-item.py

update-box-db :
	python3.11 bin/box_data/update-box-db.py