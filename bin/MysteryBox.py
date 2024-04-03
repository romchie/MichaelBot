# this will be a michael zombie mystery box simulator
# still early development

import random
import time

import discord

class MysteryBox:
    def __init__(self, client):
        self.client = client
        self.items = ['MP5', 'AK47', 'AK74u', 'Ray Gun', 'LSAT']

    def spinBox(self):
        return random.choice(self.items)
    
