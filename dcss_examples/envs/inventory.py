import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import random
import sys
sys.path.append("dcss_examples/envs/")
from item import Item
"""
TODO:
Sort inventory by AC/EV/etc... and figure out max AC etc.
Actually get reward function going
-This includes doing the dodging and EV formulas


"""
class InventoryEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array", "None"], "render_fps": 4}

    def __init__(self, render_mode=None, verbose_output = False, max_iterations = 100):
        self.size = 341  # The size of our observation space - AC, EV, SH, ATTSP, ATT, STR, INT, DEX, SKILL:SH, SKILL:AC, SKILL: EV
        self.window_size = 512  # The size of the PyGame window

        self.verbose_output = verbose_output
        self.iteration = 0 #Which turn we're on
        self.max_iterations = max_iterations# End of episode
        #Set all of our stats. I can move this to a dict should I feel like it
        self.AC = 0
        self.EV = 0
        self.SH = 0
        self.ATT = 0
        self.ATTSP = 0
        self.ENC = 0
        self.STR = 0
        self.INT = 0
        self.DEX = 0
        self.SKSH = 0
        self.SKAC = 0
        self.SKEV = 0



        #Set the stats for our current character - they'll be static for now
        self._randomize_stats()

        #List containing our items - will be full of random objects at first. Will add in other features later
        self.inventory = [None] * 59 #Just filling with nothing for now - will be filled with inventory items later

        self._set_up_random_inventory()

        #Start with randomized inventory to spice things update
        self.currently_equipped = [None] * 7

        #for i in range(7):
            #self.currently_equipped[i] = random.choice(self.inventory)


        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).

        self.observation_space = spaces.Dict(
            {
                "AC": spaces.Discrete(101),
                "EV": spaces.Discrete(101),
                "ATT": spaces.Discrete(20),
                "ATTSP": spaces.Discrete(20),
                "STR": spaces.Discrete(40),
                "INT": spaces.Discrete(40),
                "DEX": spaces.Discrete(40),
                "SKAC": spaces.Discrete(27),
                "SKSH": spaces.Discrete(27),
                "SKEV": spaces.Discrete(27),
                "HelmetAC": spaces.Discrete(20),
                "BootsAC": spaces.Discrete(20),
                "CapeAC": spaces.Discrete(20),
                "GlovesAC": spaces.Discrete(20),
                "BodyAC": spaces.Discrete(20),
                "HelmetENC": spaces.Discrete(20),
                "BootsENC": spaces.Discrete(20),
                "CapeENC": spaces.Discrete(20),
                "GlovesENC": spaces.Discrete(20),
                "BodyENC": spaces.Discrete(20),
                "ShieldENC": spaces.Discrete(20),
                "ShieldSH": spaces.Discrete(20),
                "HelmetEV": spaces.Discrete(20),
                "BootsEV": spaces.Discrete(20),
                "CapeEV": spaces.Discrete(20),
                "GlovesEV": spaces.Discrete(20),
                "BodyEV": spaces.Discrete(20),
                "WeaponATT": spaces.Discrete(20),
                "WeaponATTSP": spaces.Discrete(20)
            }
        )

        for i in range(52):
            self.observation_space.__setitem__("item_"+str(i)+"_AC", spaces.Discrete(20))
            self.observation_space.__setitem__("item_"+str(i)+"_EV", spaces.Discrete(20))
            self.observation_space.__setitem__("item_"+str(i)+"_ENC", spaces.Discrete(20))
            self.observation_space.__setitem__("item_"+str(i)+"_SH", spaces.Discrete(20))
            self.observation_space.__setitem__("item_"+str(i)+"_ATT", spaces.Discrete(20))
            self.observation_space.__setitem__("item_"+str(i)+"_ATTSP", spaces.Discrete(20))

        # My action space will be:
        """
        Action Space of 60:
        Equip item in slot a
        ... b
        ... ...
        ... z
        ... A
        ... B
        ... ...
        ... Z
        Unequip Helmet
        Unequip Shield
        Unequip Body
        Unequip Boots
        Unequip Gloves
        Unequip Cape
        Unequip Weapon
        Do Nothing
        """
        self.action_space = gym.spaces.Discrete(60)


        #assert render_mode is None
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None

    def _set_up_random_inventory(self):
        perfects = []
        for i in range(5):
            perfects.append(random.choice(range(52)))
        slot_iterator = 0
        for i in range(52):
            if i in perfects:
                self.inventory[i] = Item("perfect",slot_iterator, 19, 0, 0, 0, 19, 19)
                slot_iterator += 1
            else:
                self.inventory[i] = Item("dummy", "dummy")
                self.inventory[i].generate_random_item()

    def _randomize_stats(self):
        self.STR = random.choice(range(40))
        self.INT = random.choice(range(40))
        self.DEX = random.choice(range(40))
        self.SKSH = random.choice(range(27))
        self.SKAC = random.choice(range(27))
        self.SKEV = random.choice(range(27))

    def _equip_item(self, item, slot = None): #If passing in none, must pass in the slot as well
        #Get which slot I'm talking about
        if item is not None:
            slot = item.item_type
        #If I have something there already, unequip it
        if self.currently_equipped[slot] is not None:
            self._change_stats(self.currently_equipped[slot], -1)
        #Equip my item and add its stats
        self.currently_equipped[slot] = item
        self._change_stats(self.currently_equipped[slot], 1)

    def _change_stats(self, item, operator):#-1 for subtract 1 for add if item is none then do nothing
        if item is None:
            self.AC += 0
            self.EV += 0
            self.SH += 0
            self.ATT += 0
            self.ATTSP += 0
            self.ENC += 0
        else:
            self.AC += item.AC * operator
            self.EV += item.EV * operator
            self.SH += item.SH * operator
            self.ATT += item.ATT * operator
            self.ATTSP += item.ATTSP * operator
            self.ENC += item.ENC * operator

    def _get_obs(self):
        value_dict = {
        "AC": self.AC,
        "EV": self.EV,
        "ATT": self.ATT,
        "ATTSP": self.ATTSP,
        "STR": self.STR,
        "INT": self.INT,
        "DEX": self.DEX,
        "SKAC": self.SKAC,
        "SKSH": self.SKSH,
        "SKEV": self.SKEV,
        "HelmetAC": 0,
        "BootsAC": 0,
        "CapeAC": 0,
        "GlovesAC": 0,
        "BodyAC": 0,
        "HelmetENC": 0,
        "BootsENC": 0,
        "CapeENC": 0,
        "GlovesENC": 0,
        "BodyENC": 0,
        "ShieldENC": 0,
        "ShieldSH": 0,
        "HelmetEV": 0,
        "BootsEV": 0,
        "CapeEV": 0,
        "GlovesEV": 0,
        "BodyEV": 0,
        "WeaponATT": 0,
        "WeaponATTSP": 0
        }

        for i in range(7):
            if self.currently_equipped[i] is not None:
                if i == 0:
                    value_dict.update({"HelmetAC": self.currently_equipped[i].AC})
                    value_dict.update({"HelmetEV": self.currently_equipped[i].EV})
                    value_dict.update({"HelmetENC": self.currently_equipped[i].ENC})
                elif i == 1:
                    value_dict.update({"BootsAC": self.currently_equipped[i].AC})
                    value_dict.update({"BootsEV": self.currently_equipped[i].EV})
                    value_dict.update({"BootsENC": self.currently_equipped[i].ENC})
                elif i == 2:
                    value_dict.update({"CapeAC": self.currently_equipped[i].AC})
                    value_dict.update({"CapeEV": self.currently_equipped[i].EV})
                    value_dict.update({"CapeENC": self.currently_equipped[i].ENC})
                elif i == 3:
                    value_dict.update({"GlovesAC": self.currently_equipped[i].AC})
                    value_dict.update({"GlovesEV": self.currently_equipped[i].EV})
                    value_dict.update({"GlovesENC": self.currently_equipped[i].ENC})
                elif i == 4:
                    value_dict.update({"BodyAC": self.currently_equipped[i].AC})
                    value_dict.update({"BodyEV": self.currently_equipped[i].EV})
                    value_dict.update({"BodyENC": self.currently_equipped[i].ENC})
                elif i == 5:
                    value_dict.update({"ShieldSH": self.currently_equipped[i].SH})
                    value_dict.update({"ShieldENC": self.currently_equipped[i].ENC})
                elif i == 6:
                    value_dict.update({"WeaponATT": self.currently_equipped[i].ATT})
                    value_dict.update({"WeaponATTSP": self.currently_equipped[i].ATTSP})

        for i in range(52):
            value_dict.update({"item_"+str(i)+"_AC":self.inventory[i].AC})
            value_dict.update({"item_"+str(i)+"_EV":self.inventory[i].EV})
            value_dict.update({"item_"+str(i)+"_ENC":self.inventory[i].ENC})
            value_dict.update({"item_"+str(i)+"_SH":self.inventory[i].SH})
            value_dict.update({"item_"+str(i)+"_ATT":self.inventory[i].ATT})
            value_dict.update({"item_"+str(i)+"_ATTSP":self.inventory[i].ATTSP})
        return value_dict

    def _get_info(self):
        return {"items": self.inventory, "equipped": self.currently_equipped}

    def _get_reward(self, terminated, action):
        """
        TODO: DETERMINE REWARDS IDEAS
        For now I'll do sum of stats, but I should be using the actual dcss equations here
        I think I just find my base evasion then apply armor/shield penalties to it
        Do the same with AC

        """
        reward = 0

        if terminated:
            #print(terminated)
            #for i in range(len(self.currently_equipped)):
            #    if self.currently_equipped[i] is None:
            #        reward -= 100
            #reward += (self.AC + self.EV + self.ATT + self.ATTSP - self.ENC + self.SH)
            reward = self.AC * (self.SKAC/(26+self.ENC)) + self.EV * (self.SKEV/(26+self.ENC)) + self.SH * (self.SKSH/(26+self.ENC)) + self.ATT * (1/(1+self.ATTSP))
            if self.verbose_output is True:
                with open('logs/terminated_logs.txt','a') as f:
                    for i in range(7):
                        if self.currently_equipped[i] is not None:
                            self.currently_equipped[i].print_stats(f)
                    print("Final AC: ", self.AC, "\nFinal EV: ", self.EV, "\nFinal SH: ", self.SH, "\nFinal ENC: ", self.ENC, "\nFinal ATT: ", self.ATT, "\nFinal ATTSP: ", self.ATTSP, "\nFinal SKAC: ", self.SKAC,
                    "\nFinal SKEV: ", self.SKEV, "\nFinal SKSH: ", self.SKSH, "\nFinal Reward: ", reward, file=f)
                f.close()

        return reward

    def toggle_verbose_output(self):
        self.verbose_output = True

    def print_current_stats(self):
        if self.iteration >= self.max_iterations:
            print("Final AC: ", self.AC, "\nFinal EV: ", self.EV, "\nFinal SH: ", self.SH, "\nFinal ENC: ", self.ENC, "\nFinal ATT: ", self.ATT, "\nFinal ATTSP: ", self.ATTSP)

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        #Reset all of our items to nothing
        for i in range(len(self.currently_equipped)):
            #if self.currently_equipped[i] is not None:
                #self.currently_equipped[i].print_stats()
            self._equip_item(None, i)
        #Randomize our stats for another go around
        self._randomize_stats()
        self.iteration = 0
        #Base observation should be all 0's
        observation = self._get_obs()
        #Base info should be turn 0
        info = self._get_info()


        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        #Equip a given item based on the action received
        #print("Got action: ", action)
        if action == 59:
            #print("Doing Nothing")
            pass
        elif action > 51 and action < 59: #Must be equipping nothing
            #print("Unequipping item")
            self._equip_item(self.inventory[action], -1 * (52 - action))
        else:
            #print("Equipping item")
            self._equip_item(self.inventory[action])

        self.iteration += 1
        terminated = (self.iteration >= self.max_iterations)

        reward = self._get_reward(terminated, action)
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        if self.render_mode == "None":
            return "All done!"

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
