import json

FILE = 'bin/box_data/box_items.json'


def readDataBase():
        with open(FILE, 'r') as file:
            return json.load(file)
        
def writeDataBase(data):
    with open(FILE, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    db = readDataBase()
    for item_type in db['box_items']['types']:
        items = db['box_items'][item_type]['items']
        for item in items:
            db['box_items']['items'][item['name']] = item
            db['box_items']['items'][item['name']]['item_type'] = item_type
    writeDataBase(db)