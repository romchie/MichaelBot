import json

FILE = 'data/inventories.json'


def readDataBase():
        with open(FILE, 'r') as file:
            return json.load(file)
        
def writeDataBase(data):
    with open(FILE, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    db = readDataBase()
    user_arr = []
    usernames = list(db['users'])
    for username in usernames:
        user_arr.append(db['users'][username])
    
    db['users'] = {}

    for i, user in enumerate(user_arr):
        new_user_obj = {
            'username': usernames[i],
            'id': user['id'],
            'mpoints': user['mpoints'],
            'fpoints': user.get('fpoints', 0),
            'items': user['guns']
        }
        db['users'][user['id']] = new_user_obj
    
    writeDataBase(db)
    