"""
TODO: DEFINE ITEM CLASS
Needs AC value, SH value, weight, type (helmet/body/weapon/etc)
May have to split into armor and weapon classes
"""
import random
class Item():
    """
    Name is a string saying the name eg 'Plate Armor'/'Ring Mail'/etc
    Item type is the slot it goes in: 
    0: Helmet
    1: Boots
    2: Cape
    3: Gloves
    4: Body
    5: Shield
    6: Weapon
    The rest are the stats of the item
    """
    
    def __init__(self, name, item_type, AC = 0, SH = 0, ATT = 0, ATTSP = 0, ENC = 0, EV = 0):
        self.name = name
        self.item_type = item_type
        self.AC = AC
        self.SH = SH
        self.EV = EV
        self.ATT = ATT
        self.ATTSP = ATTSP
        self.ENC = ENC
        
    def generate_random_item(self):
        self.item_type = random.choice(range(7))
        if self.item_type < 5:
            self.AC = random.choice(range(20))
            self.ENC = random.choice(range(20))
            self.EV = random.choice(range(20))
        elif self.item_type == 6:
            self.ATT = random.choice(range(20))
            self.ATTSP = random.choice(range(20))
        else:
            self.SH = random.choice(range(20))
            self.ENC = random.choice(range(20))
    
    def print_stats(self, f):
        print("Name: ", self.name, "\nType: ", self.item_type, "\nAC: ", self.AC, "\nEV: ", self.EV, "\nSH: ", self.SH, "\nATT: ", self.ATT, "\nATTSP: ", self.ATTSP, "\nENC: ", self.ENC, file=f)
        