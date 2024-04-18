import random
import json
import discord

class MysteryBox:
    def __init__(self):
        self.INVENTORY_FILE = 'data/inventories.json'
        self.BOX_ITEMS_FILE = 'bin/box_data/box_items.json'
        self.db_clear_types = ['all', 'guns', 'mpoints']

        self.assault_rifles = ['AK47', 'AUG A1', 'FG42', 'M4A4', 'STG-44', 'M16-M', 'Famas F1']
        self.carbines = ['Gewer 43', 'M1A1 Carbine', 'M1 Garand', 'M14']
        self.smgs = ['AK-74u', 'MP40', 'MP5', 'PPSH', 'M1 Thompson', 'Type 100']
        self.lmgs = ['B.A.R', 'M1919 Browning', 'LSAT', 'MG42', 'RPK']
        self.shotguns = ['Sawed-Off', 'Model 680 Shotgun', 'Saiga-12', 'Trench Shotgun', 'Super-Shorty']
        self.snipers = ['Kar98k', 'PTRS-41']
        self.side_arms = ['B93 Raffica', 'M1911 Colt', '.357 Magnum', 'Mauser C96', 'Walther P99', 'Desert Eagle']
        self.specials = ['M2 Flamethrower', 'Panzerschrek', 'Raygun', 'Wunderwaffe DG-2']
        self.melees = ['Knife', 'Bowie Knife', 'Oar', 'Frying Pan']
        self.uniques = ['Michael']
        self.items = self.assault_rifles + self.carbines + self.smgs + self.lmgs + self.shotguns + self.snipers + self.side_arms + self.specials + self.melees + self.uniques

    def readDataBase(self, infile: str) -> any:
        with open(infile, 'r') as file:
            return json.load(file)
        
    def writeDataBase(self, data, infile: str) -> None:
        with open(infile, 'w') as file:
            json.dump(data, file, indent=4)

    def clearDataBase(self, t:str='all'):
        """Types: `all`, `guns`, `mpoints`"""
        db = self.readDataBase(self.INVENTORY_FILE)
        if t == 'all':
            print('clearing all...')
            db['users'] = {}
        elif t == 'guns':
            print('clearing guns...')
            for user in db['users']:
                db['users'][user]['guns'] = []
        elif t == 'mpoints':
            print('clearing michael points...')
            for user in db['users']:
                user['mpoints'] = 0
        self.writeDataBase(db, self.INVENTORY_FILE)

    def addUser(self, user: discord.User, database) -> None:
        if str(user) not in database['users']:
            database['users'][str(user)] = {
                "id": user.id,
                "mpoints": 0,
                "fpoints": 0,
                "guns": [],
            }

    def spinBox(self, user: discord.User) -> discord.Embed:
        inventory_db = self.readDataBase(self.INVENTORY_FILE)
        box_db = self.readDataBase(self.BOX_ITEMS_FILE)
        self.addUser(user, inventory_db)

        item_types = list(box_db['box_items']['types'])
        item_type_weights = [box_db['box_items'][itype]['weight'] for itype in item_types]
        item_type = random.choices(population=item_types, weights=item_type_weights)[0]
        items = list(box_db['box_items'][item_type]['items'])
        item_weights = [item['weight'] for item in items]
        item_data = random.choices(population=items, weights=item_weights)[0]
        item_name = item_data['name']
        item_mp = item_data['mpoints_value']
        item_rarity = item_data['rarity']

        e = discord.Embed(title=item_name, description=item_rarity.capitalize() + f' • `{item_mp} mp`', color=box_db['box_items']['colors'][item_rarity])
        e.set_image(url=item_data['img_url'])
        # e.add_field(name=f'{item_mp} mp', value='')

        if item_name in inventory_db['users'][str(user)]['guns']:
            e.set_footer(text=f'You\'ve already GYAT one!', icon_url='https://cdn.inspireuplift.com/uploads/images/seller_products/31661/1702901872_MetalGearSolidAlert.png')
        else:
            e.set_footer(text='You rolled a new item!', icon_url='https://png.pngtree.com/png-vector/20221215/ourmid/pngtree-green-check-mark-png-image_6525691.png')
            inventory_db['users'][str(user)]['guns'].append(item_name)
            self.writeDataBase(inventory_db, self.INVENTORY_FILE)

        return e
    
    def showInventory(self, user: discord.User) -> str:
        db = self.readDataBase(self.INVENTORY_FILE)
        if str(user) not in db['users'] or len(db['users'][str(user)]['guns']) == 0:
            return f'ya shit\'s EMPTY'
        user_guns = db['users'][str(user)]['guns']
        gun_list = '```'
        for gun in user_guns:
            gun_list += f'• {gun}\n'
        gun_list += '```'
        return f'**{str(user)}\'s Inventory: ({len(user_guns)}/{len(self.items)} collected)**\n{gun_list}'

    def getMichaelPoints(self, user: discord.User) -> int:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        michael_points = db['users'][str(user)].get('mpoints', 0)
        return michael_points
    
    def getFreakyPoints(self, user: discord.User) -> int:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        freaky_points = db['users'][str(user)].get('fpoints', 0)
        return freaky_points
    
    def updateMichaelPoints(self, user: discord.User, val: int) -> str:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        db['users'][str(user)]['mpoints'] = db['users'][str(user)].get('mpoints', 0) + val
        self.writeDataBase(db, self.INVENTORY_FILE)
        if val > 0:
            return f'+{val} Michael Points'
        elif val < 0:
            return f'{val} Michael Points'
        
    def updateFreakyPoints(self, user: discord.User, val: int) -> str:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        db['users'][str(user)]['fpoints'] = db['users'][str(user)].get('fpoints', 0) + val
        self.writeDataBase(db, self.INVENTORY_FILE)
        if val > 0:
            return f'+{val} Freaky Points'
        elif val < 0:
            return f'{val} Freaky Points'

    def showLeaderboard(self, board_type: str='mpoints') -> str:
        """`board_type`: `mpoints` or `fpoints`"""
        if board_type in ['mpoints', 'fpoints']:
            db = self.readDataBase(self.INVENTORY_FILE)
            points_arr = []
            for data in list(db['users'].items()):
                points_arr.append({'user': data[0], board_type: data[1].get(board_type, 0)})
            sorted_order = sorted(points_arr, key=lambda x: x[board_type], reverse=True)
            leaderboard_str = '**Michael Points Leaderboard**\n```' if board_type == 'mpoints' else '**Freaky Points Leaderboard**\n```'
            rank = 1
            for data in sorted_order:
                username = data['user']
                points = data[board_type]
                if points != 0:
                    currency = 'mp' if board_type == 'mpoints' else 'fp'
                    leaderboard_str += f'{rank}) {points} {currency} - {username}\n'
                    rank += 1
            leaderboard_str += '```'
            return leaderboard_str
        else:
            print('incorrect or no leaderboard type provided')

    def hasHeadphones(self, user: discord.User) -> bool:
        db = self.readDataBase(self.INVENTORY_FILE)
        if 'Headphones' in db['users'][str(user)]['guns']:
            return True
        return False
    
    def hasItem(self, user: discord.User, item: str) -> bool:
        db = self.readDataBase(self.INVENTORY_FILE)
        if item in db['users'][str(user)]['guns']:
            return True
        return False
    
    def sellItem(self, user: discord.User, item: str):
        inventory_db: dict = self.readDataBase(self.INVENTORY_FILE)
        box_db: dict = self.readDataBase(self.BOX_ITEMS_FILE)
        if self.hasItem(user, item):
            mp_value = box_db['box_items']['items'][item]['mpoints_value']
            inventory_db['users'][str(user)]['guns'].remove(item)
            self.writeDataBase(inventory_db, self.INVENTORY_FILE)
            self.updateMichaelPoints(user, mp_value)
            return item, mp_value
        else:
            return None, None


class Items(MysteryBox):
    def __init__(self):
        super().__init__()



class Item(Items):
    def __init__(self):
        super().__init__()
