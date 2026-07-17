import random
import json
import discord
from assets.CustomEmoji import *

class MysteryBox:
    def __init__(self):
        self.INVENTORY_FILE = 'data/inventories.json'
        self.BOX_ITEMS_FILE = 'bin/box_data/box_items.json'
        self.db_clear_types = ['all', 'guns', 'mpoints']

    def readDataBase(self, infile: str) -> any:
        with open(infile, 'r') as file:
            return json.load(file)
        
    def writeDataBase(self, data, infile: str) -> None:
        with open(infile, 'w') as file:
            json.dump(data, file, indent=4)

    def clearDataBase(self, t:str='all'):
        """Types: `all`, `items`, `mpoints`"""
        db = self.readDataBase(self.INVENTORY_FILE)
        if t == 'all':
            print('clearing all...')
            db['users'] = {}
        elif t == 'items':
            print('clearing items...')
            for user in db['users']:
                db['users'][user]['items'] = []
        elif t == 'mpoints':
            print('clearing michael points...')
            for user in db['users']:
                user['mpoints'] = 0
        self.writeDataBase(db, self.INVENTORY_FILE)

    def addUser(self, user: discord.User, database) -> None:
        if str(user.id) not in database['users']:
            database['users'][str(user.id)] = {
                "username": str(user),
                "id": user.id,
                "mpoints": 0,
                "fpoints": 0,
                "items": [],
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

        e = discord.Embed(title=item_name, description=item_rarity.capitalize() + f' • {item_mp}{MP_EMOJI}', color=box_db['box_items']['colors'][item_rarity])
        e.set_image(url=item_data['img_url'])
        # e.add_field(name=f'{item_mp} mp', value='')

        if item_name in inventory_db['users'][str(user.id)]['items']:
            e.set_footer(text=f'You\'ve already GYAT one!', icon_url='https://cdn.inspireuplift.com/uploads/images/seller_products/31661/1702901872_MetalGearSolidAlert.png')
        else:
            e.set_footer(text='You rolled a new item!', icon_url='https://png.pngtree.com/png-vector/20221215/ourmid/pngtree-green-check-mark-png-image_6525691.png')
            inventory_db['users'][str(user.id)]['items'].append(item_name)
            self.writeDataBase(inventory_db, self.INVENTORY_FILE)

        return e
    
    def showInventory(self, user: discord.User) -> discord.Embed:
        db = self.readDataBase(self.INVENTORY_FILE)
        box_db = self.readDataBase(self.BOX_ITEMS_FILE)
        all_items = box_db['box_items']['items']
        colors = box_db['box_items']['colors']

        if str(user.id) not in db['users'] or len(db['users'][str(user.id)]['items']) == 0:
            e = discord.Embed(description="ya shit's EMPTY", color=colors['common'])
            return e

        user_items = db['users'][str(user.id)]['items']

        rarity_order = ['mythic', 'legendary', 'epic', 'rare', 'uncommon', 'common']
        rarity_labels = {
            'mythic':    '✦ Mythic',
            'legendary': '★ Legendary',
            'epic':      '◆ Epic',
            'rare':      '● Rare',
            'uncommon':  '○ Uncommon',
            'common':    '· Common',
        }

        # Group items by rarity
        grouped: dict[str, list] = {r: [] for r in rarity_order}
        for item_name in user_items:
            item_data = all_items.get(item_name)
            if item_data:
                rarity = item_data.get('rarity', 'common')
                mp = item_data.get('mpoints_value', 0)
            else:
                rarity = 'common'
                mp = 0
            grouped[rarity].append((item_name, mp))

        # Pick embed color from the rarest group the user owns
        embed_color = colors['common']
        for rarity in rarity_order:
            if grouped[rarity]:
                embed_color = colors[rarity]
                break

        e = discord.Embed(
            title=f"{str(user)}'s Inventory",
            description=f'{len(user_items)} item{"s" if len(user_items) != 1 else ""} collected',
            color=embed_color,
        )

        for rarity in rarity_order:
            items_in_group = grouped[rarity]
            if not items_in_group:
                continue
            lines = '\n'.join(f'`{name}` — {mp}{MP_EMOJI}' for name, mp in items_in_group)
            e.add_field(name=rarity_labels[rarity], value=lines, inline=False)

        return e

    def getMichaelPoints(self, user: discord.User) -> int:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        michael_points = db['users'][str(user.id)].get('mpoints', 0)
        return michael_points
    
    def getFreakyPoints(self, user: discord.User) -> int:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        freaky_points = db['users'][str(user.id)].get('fpoints', 0)
        return freaky_points
    
    def updateMichaelPoints(self, user: discord.User, val: int) -> str:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        db['users'][str(user.id)]['mpoints'] = db['users'][str(user.id)].get('mpoints', 0) + val
        self.writeDataBase(db, self.INVENTORY_FILE)
        if val > 0:
            return f'+{val} Michael Points'
        elif val < 0:
            return f'{val} Michael Points'
        
    def updateFreakyPoints(self, user: discord.User, val: int) -> str:
        db = self.readDataBase(self.INVENTORY_FILE)
        self.addUser(user, db)
        db['users'][str(user.id)]['fpoints'] = db['users'][str(user.id)].get('fpoints', 0) + val
        self.writeDataBase(db, self.INVENTORY_FILE)
        if val > 0:
            return f'+{val} Freaky Points'
        elif val < 0:
            return f'{val} Freaky Points'

    def showLeaderboard(self, board_type: str='mpoints') -> discord.Embed:
        """`board_type`: `mpoints` or `fpoints`"""
        if board_type in ['mpoints', 'fpoints']:
            db = self.readDataBase(self.INVENTORY_FILE)
            points_arr = []

            e = discord.Embed(title='Michael Points Leaderboard', color=4247121)
            e.set_thumbnail(url='https://i.imgur.com/HRS8Ews.png')

            for data in list(db['users'].items()):
                points_arr.append({'user': data[0], board_type: data[1].get(board_type, 0)})
            sorted_order = sorted(points_arr, key=lambda x: x[board_type], reverse=True)
            # leaderboard_str = '**Michael Points Leaderboard**\n```' if board_type == 'mpoints' else '**Freaky Points Leaderboard**\n```'
            leaderboard_str = ''
            rank = 1
            for data in sorted_order:
                username = db['users'][data['user']]['username']
                points = data[board_type]
                if points != 0:
                    currency = MP_EMOJI if board_type == 'mpoints' else 'fp'
                    if rank < 10:
                        leaderboard_str += f'{rank}.  **{username}** - {points}{currency}\n'
                    rank += 1
            e.add_field(name='', value=leaderboard_str, inline=False)
            # leaderboard_str += '```'

            return e

        else:
            print('incorrect or no leaderboard type provided')

    def hasHeadphones(self, user: discord.User) -> bool:
        db = self.readDataBase(self.INVENTORY_FILE)
        if 'Headphones' in db['users'][str(user.id)]['items']:
            return True
        return False
    
    def hasItem(self, user: discord.User, item: str) -> bool:
        db = self.readDataBase(self.INVENTORY_FILE)
        if item in db['users'][str(user.id)]['items']:
            return True
        return False
    
    def sellItem(self, user: discord.User, item: str):
        inventory_db: dict = self.readDataBase(self.INVENTORY_FILE)
        box_db: dict = self.readDataBase(self.BOX_ITEMS_FILE)
        if self.hasItem(user, item):
            mp_value = box_db['box_items']['items'][item]['mpoints_value']
            inventory_db['users'][str(user.id)]['items'].remove(item)
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
