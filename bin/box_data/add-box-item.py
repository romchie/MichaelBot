import json

FILE = 'bin/box_data/box_items.json'


def readDataBase():
        with open(FILE, 'r') as file:
            return json.load(file)
        
def writeDataBase(data):
    with open(FILE, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    go_again = True
    while go_again:
        db = readDataBase()
        print("\nItem Types:")
        for item_type in db['box_items']['types']:
            print(f'> {item_type}')
        chosen_type = input("\nEnter item type: ")
        if chosen_type in db['box_items']['types']:
            print("Fill out the following fields:")
            name = input('> item name: ')
            rarity = input('> rarity: ')
            weight = input('> roll weight: ')
            mpoints_value = input('> mp value: ')
            img_url = input('> image url: ')
            new_item = {
                "name": name,
                "rarity": rarity,
                "weight": int(weight),
                "mpoints_value": int(mpoints_value),
                "img_url": img_url
            }
            db['box_items'][chosen_type]['items'].append(new_item)
            writeDataBase(db)
            print('item added')
        else:
            print('Not a valid item type')
        if input('\nAdd another item? (y/n): ') == 'n':
            go_again = False
