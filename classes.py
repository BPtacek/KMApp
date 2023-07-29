# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:40:22 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
from constants import *


class Kingdom:
    def __init__(self, name="", claimed_hexes=[], level=1, unrest=0, ruins={i:0 for i in Ruins}, 
                 settlements = [], attributes = {i:10 for i in Kingdom_skills.values()}, 
                 skills={i:0 for i in Kingdom_skills.keys()}, advisors={i:"filled" for i in Advisors.keys()}, 
                 relations={},RP=[0,0,0],xp=0,work_camps={},capital="",
                 resources={"food":[0,0,0],"lumber":[0,0,0],"ore":[0,0,0],"stone":[0,0,0],"luxuries":[0,0,0]}):
        self.name = name  # String, Kingdom name
        self.claimed_hexes = claimed_hexes  # List of tuples (x,y) specifying coordinates of claimed hexes
        self.level = level  # Int, kingdom level
        self.unrest = unrest  # Int, kingdom's level of unrest
        self.settlements = settlements  # List of Settlement objects representing kingdom's settlements
        self.ruins = ruins  # Dictionary, names and values of kingdom's ruins
        self.attributes = attributes  # Dictionary, names and values of kingdom's attributes
        self.skills = skills  # Dictionary, {skill name (str): kingdom proficiency value (int, 0 to 4)}
        self.relations = relations  # Dictionary, names and status of diplomatic relations with neighbouring entities
        self.control_DC = control_DC_table[level] + self.get_size()
        self.advisors = advisors  # Dict {leadership role: filled/vacant}
        self.RP = RP  # List [Int, Int, Int] - current RP, size of resource die, number to roll next turn
        self.resources = resources  # Dict {"resource name":[stored amount, storage capacity, gain next turn]}
        # resources are Food, Lumber, Stone, Ore, and Luxuries
        self.xp = xp # Int, current XP
        self.work_camps = work_camps # Dict, {work camp object:[list of hex coordinates]}
        self.capital = capital # String, identity of Kingdom's capital
        
    def set_name(self,name):
        self.name = name
        
    def set_attributes(self,attributes):
        self.attributes = attributes
        
    def set_skills(self,skills):
        self.skills = skills
        
    def set_unrest(self,unrest):
        self.unrest=unrest
        
    def set_ruins(self,ruins):
        self.ruins = ruins
        
    def set_settlements(self,settlements):
        self.settlements = settlements
    
    def set_RP(self,rp):
        self.RP=rp
        
    def set_advisors(self,advisors):
        self.advisors = advisors
    
    def set_xp(self,xp):
        self.xp = xp
        
    def set_resources(self,resources):
        self.resources = resources
        
    def set_capital(self,capital):
        if self.settlements != []:
            settlement_names = [i.name for i in self.settlements]
            if capital in settlement_names:
                self.capital=capital
                
    def set_work_camps(self,work_camps):
        self.work_camps = work_camps
        
    def set_level(self,level):
        self.level = level
        
    def set_relations(self,relations):
        self.relations = relations
    
    def add_settlement(self,name,location,buildings):
        s = Settlement(name,location,buildings)
        self.settlements.append(s)
    
    def reset(self):
        self.claimed_hexes = []
        self.settlements = []
        self.level = 1
        self.update_control_DC()
        self.skills = {i:0 for i in Kingdom_skills.keys()}
        self.attributes = {i:10 for i in Kingdom_skills.values()}
        self.ruins = {i:0 for i in Ruins}
        self.xp = 0
        self.RP = [0,4,9]
        self.work_camps = {"farms":0,"lumber camps":0,"mines":0,"quarries":0}        
        self.name = ""
        self.resources = {"food":[0,0,0],"lumber":[0,0,0],"stone":[0,0,0],"ore":[0,0,0],"luxuries":[0,0,0]}
        self.capital = None
        

    def update_control_DC(self):
        self.control_DC = control_DC_table[self.level] + self.get_size()
        
    def get_base_resource_die_string(self):
        if len(self.claimed_hexes) < 1: die_size = 0
        else: die_size = max([j["rd size"] for (i, j) in size_thresholds.items() if i < len(self.claimed_hexes)])
        return str(self.level + 4) + "d" + str(die_size)

    def increase_level(self):
        if self.level < 20:
            self.level += 1
            self.update_control_DC()
        else:
            print("Kingdom level cannot exceed 20!")

    def get_unrest_penalty(self):
        penalties = {0:0,1:1,5:2,10:3,15:4}
        return max([penalties[i] for i in penalties.keys() if self.unrest >= i])

    def reduce_level(self):
        if self.level > 1:
            self.level -= 1
            self.update_control_DC()
        else:
            print("Kingdom level cannot be below 1!")

    def increase_skill(self, skill):
        if self.skills[skill.lower()] < 4:
            self.skills[skill.lower()] += 1
        else:
            print("Cannot raise skill proficiency above 4!")

    def reduce_skill(self, skill):
        if self.skills[skill.lower()] < 1:
            print("Cannot reduce skill below 0!")
        else:
            self.skills[skill.lower()] -= 1

    def get_skill(self, skill):
        if skill.lower() in self.skills:
            return self.skills[skill.lower()]
        else:
            print("Skill not in skill list!")

    def increase_attribute(self, attribute):
        if attribute.lower() in self.attributes and self.attributes[attribute.lower()] < 18:
            self.attributes[attribute.lower()] += 2
        elif attribute.lower() in self.attributes and self.attributes[attribute.lower()] >= 18:
            self.attributes[attribute.lower()] += 1
        else:
            print("Either attribute was mis-spelled or you tried to reduce it below 10. Don't do those things.")

    def reduce_attribute(self, attribute):
        if attribute.lower() in self.attributes and self.attributes[attribute.lower()] > 10:
            if self.attributes[attribute.lower()] > 18:
                self.attributes[attribute.lower()] -= 1
            else:
                self.attributes[attribute.lower()] -= 2
        else:
            print("Cannot reduce attribute below 10")

    def get_attribute(self, attribute):
        if attribute.lower() in self.attributes:
            return self.attributes[attribute.lower()]
        else:
            print("The input attribute was not in the attribute list, you should fix that.")

    def change_ruin(self, ruin, change):
        if ruin.lower() in self.ruins:
            if self.ruins[ruin.lower()] + change < 0:
                self.ruins[ruin.lower()] = 0
            else:
                self.ruins[ruin.lower()] += change

    def change_unrest(self, change):
        try: change = int(change)
        except: return "Value submitted to kingdom.change_unrest() could not be converted to an integer"
        if self.unrest + change < 0:
            self.unrest = 0
        else:
            self.unrest += change

    def add_hex(self, coordinates):
        # coordinates is a tuple, (x,y)
        if coordinates not in self.claimed_hexes:
            self.claimed_hexes.append(coordinates)
            self.update_control_DC()
        else:
            print("You tried to add a hex that already belongs to the kingdom. That was pretty dumb.")

    def remove_hex(self, coordinates):  # coordinates is a tuple (x,y) - a set of hex grid coordinates
        if coordinates in self.claimed_hexes:
            self.claimed_hexes.remove(coordinates)
            self.update_control_DC()
        else:
            print("You tried to remove a hex that didn't belong to the kingdom to begin with.")

    def get_size(self):
        # returns the control DC modifier for the kingdom based on its number of claimed hexes
        num_hexes = len(self.claimed_hexes)
        if num_hexes == 0:
            return 0        
        elif [j["dc modifier"] for (i, j) in size_thresholds.items() if i < num_hexes] == []: return 0
        else: return max([j["dc modifier"] for (i, j) in size_thresholds.items() if i < num_hexes])

    def get_modifier(self, skill):
        # String -> Int, get the modifier (attribute + proficiency + building item + ruler circumstance) for the named skill
        skill_attribute = Kingdom_skills[skill]  # find the attribute corresponding to the named skill
        leadership_bonus = max(
            {leadership_status_bonuses[i] for i in leadership_status_bonuses.keys() if i <= self.level})
        relevant_advisors = {i: j for (i, j) in Advisors.items() if Advisors[i] == skill_attribute}
        relevant_role_filled = True in [self.advisors[i] == "filled" for i in relevant_advisors.keys()]
        level_multiplier = self.level * (self.get_skill(skill) != 0)  # Int * Bool
        proficiency_bonus = 2 * self.get_skill(skill)
        attribute_bonus = (self.get_attribute(Kingdom_skills[skill]) - 10) // 2
        leadership_bonus = leadership_bonus * relevant_role_filled  # Int * Bool
        return level_multiplier + proficiency_bonus + attribute_bonus + leadership_bonus - self.get_unrest_penalty()

    def skill_check(self, skill):
        # string -> Int, roll a check against the named skill
        return d20() + self.get_modifier(skill)

    def building_modifiers(self):
        # generate a dictionary of all the bonuses to Kingdom activities provided by every building in every settlement
        out = {}
        for settlement in self.settlements:
            for bonus in settlement.kingdom_bonuses():
                if bonus in out.keys() and settlement.kingdom_bonuses()[bonus] > out[bonus]:
                    out[bonus] = settlement.kingdom_bonuses()[bonus]
                elif bonus not in out.keys():
                    out[bonus] = settlement.kingdom_bonuses()[bonus]
            return out

    def get_consumption(self):
        # generate the total food consumption of every settlement in the kingdom
        return sum([i.get_consumption() for i in self.settlements])

    def increase_xp(self,xp):
        try: xp = int(xp)
        except: print("Value entered into XP box was not an integer. Integers only tyvm!")
        if xp + self.xp > 1000:
            self.xp = self.xp + xp - 1000
            self.increase_level()
        else: self.xp += xp

    def export_kingdom_data(self):
        # export kingdom data in JSON format as dictionary
        data = self.__dict__.copy()
        kingdom_settlements = []
        tmp = {}
        for settlement in data["settlements"]:
            readable_settlement = settlement.__dict__.copy()
            if readable_settlement.get("buildings", False):
                for building in readable_settlement.get("buildings"):
                    tmp[building.name] = readable_settlement.get("buildings").get(building)
                readable_settlement["buildings"] = tmp
                tmp = {}
            kingdom_settlements.append(readable_settlement)
        data["settlements"] = kingdom_settlements
        return data 
    

class Settlement:
    def __init__(self, name, location, buildings):
        self.name = name  # String, settlement name
        self.location = location  # tuple (Int, Int) of grid coordinates specifying settlement's location        
        self.buildings = buildings  # dictionary {Building:Int} of Building objects and number in settlement
        self.occupied_lots = sum(buildings[i] * i.lots for i in buildings)  # Int, number of lots occupied
        self.occupied_blocks = (self.occupied_lots // 4) + (self.occupied_lots % 4 > 0)  # number of blocks occupied

    def add_building(self, new_building):
        self.buildings[new_building] = self.buildings.get(new_building, 0) + 1
        self.occupied_lots += new_building.lots
        self.occupied_blocks = (self.occupied_lots // 4) + (self.occupied_lots % 4 > 0)
        
    def remove_building(self,building):
        if building not in self.buildings:
           print("Something has gone badly wrong here!") 
        elif self.buildings[building] <= 1:
            del self.buildings[building]
        else: self.buildings[building] -= 1
        self.occupied_lots -= building.lots
        self.occupied_blocks = (self.occupied_lots // 4) + (self.occupied_lots % 4 > 0)

    def destroy_building(self, building):
        if building in self.buildings.keys():
            self.buildings[building] -= 1
            if Rubble in self.buildings.keys():
                self.buildings[Rubble] += 1 * building.lots
            else:
                self.buildings[Rubble] = 1 * building.lots
        else:
            print("You tried to delete a building that wasn't in the settlement's kingdom list.")

    def kingdom_bonuses(self):
        # generate a dictionary containing a list of all the Kingdom activity bonuses provided by the settlement's buildings
        out = {}
        for building in self.buildings:
            for bonus in building.kingdom_item:
                if bonus in out.keys() and building.kingdom_item[bonus] > out[bonus]:
                    out[bonus] = building.kingdom_item[bonus]
                elif bonus not in out.keys():
                    out[bonus] = building.kingdom_item[bonus]
        return out

    def readable_buildings(self):
        # generate a human-readable list of the settlement's buildings
        return {i.name: j for (i, j) in self.buildings.items()}

    def get_consumption(self):
        # self -> Int, return settlement's per-turn food consumption
        a = settlement_consumption_scaling  # renaming for convenience!
        consumption_reducers = {i: j for (i, j) in self.buildings.items() if i.consumption}
        if [i for (i,j) in a.items() if j <= self.occupied_blocks] == []: base_consumption = 0
        else: base_consumption = max([i for (i,j) in a.items() if j <= self.occupied_blocks]) 
        return max(0, base_consumption - sum(consumption_reducers.values()))

    def is_overcrowded(self):
        # self -> Bool, return False if settlement has fewer residences than occupied blocks
        residences = {i: j for (i, j) in self.buildings.items() if i.residential}
        total_residences = sum(residences.values())  # total no. residential buildings in settlement
        return total_residences < self.occupied_blocks
    
    def get_level(self):
        return self.occupied_blocks

class Building:
    def __init__(self, name, lots, level, cost, difficulty, unrest, ruins, consumption, residential,
                 kingdom_item, PC_item):
        # cost is a list [Int, Int, Int, Int, Int] - RP, Lumber, Stone, Ore, Luxuries
        # difficulty is a list [String, Int, Int] - Skill needed to build, required proficiency (0 = untrained, 3 = master), DC
        # unrest is an integer that may include the value of a dice roll
        # ruins is a list [Int, Int, Int, Int, Int] - Change in any Ruin or in Corruption, Crime, Decay, Strife
        # consumption is Boolean; True means building reduces consumption
        # residential is Boolean; True means building is residential
        # kingdom_item is a dictionary {Str:Int, Str:Int,...} specifying numerical item bonuses to Kingdom checks
        # PC_item is a dictionary {Str:Int, Str:Int,...} specifying numerical item bonuses to PC skill checks
        self.name = name  # String, name of building
        self.lots = lots  # Int, number of lots required for building
        self.level = level  # Int, level of building
        self.RP = cost[0]  # Int, RP cost of building
        self.lumber = cost[1]  # Int, lumber cost of building
        self.stone = cost[2]  # Int, stone cost of building
        self.ore = cost[3]  # Int, ore cost of building
        self.luxuries = cost[4]  # Int, luxuries cost of building
        self.skill = difficulty[0]  # String, skill needed to construct
        self.proficiency = difficulty[1]
        self.DC = difficulty[2]  # Int, DC to build
        self.unrest = unrest  # Int, Change in Unrest upon completion
        self.ruin = ruins[0]  # Int, change in any ruin upon completion
        self.corruption = ruins[1]  # Int, change in Crime upon completion
        self.crime = ruins[2]  # Int, change in Corruption upon completion
        self.decay = ruins[3]  # Int, change in Decay upon completion
        self.strife = ruins[4]  # Int, change in Decay upon completion
        self.consumption = consumption
        self.residential = residential
        self.kingdom_item = kingdom_item  # Item bonuses to Kingdom skill checks conferred by building
        self.PC_item = PC_item  # Item bonuses to PC skill checks conferred by building

class State:
    def __init__(self,kingdom,attribute_variables={},skill_modifiers={},proficiency_variables={},ruin_variables={},
                 hex_center_list = [],hex_angle=60,hexagon_side_length=30,tabs=[],headline_frames={},table_frames={},
                 kname=None):
        self.kingdom = kingdom
        self.attribute_variables = attribute_variables
        self.skill_modifiers = skill_modifiers
        self.proficiency_variables = proficiency_variables
        self.ruin_variables = ruin_variables
        self.hex_center_list = hex_center_list
        self.hex_angle = hex_angle
        self.hexagon_side_length = hexagon_side_length
        self.grid_vertical_offset = -1.4 * hexagon_side_length  # used to adjust grid position so it matches in-game map
        self.tabs = tabs # list of tk.Frame objects housinng the tabs
        self.headline_frames = headline_frames # dict of tk.Frame objects housing the headline stats at the top of each tab
        self.table_frames = table_frames # dict of tk.Frame objects housing gui tables
        self.kname = kname # StringVar representing kingdom name
        
    def update_stringvars(self):
        for (i,j) in self.attribute_variables.items():
            j.set(self.kingdom.get_attribute(i))        
        for (i,j) in self.skill_modifiers.items():
            j.set(self.kingdom.get_modifier(i))
        for (i,j) in self.ruin_variables.items():
            j.set(self.kingdom.ruins[i])
        for (i,j) in self.proficiency_variables.items():
            proficiency = prof_dict[self.kingdom.get_skill(i)]
            j.set(proficiency)
    
    def add_to_hex_center_list(self,coords):
        # coords is a tuple (x,y)
        self.hex_center_list.append(coords)
        
    def set_map_canvas(self,canvas):
        self.map_canvas = canvas
        
    def set_worldmap(self,image):
        self.worldmap = image
        
    def set_tabs(self,tabs):
        self.tabs = tabs
    
    def set_main_header(self,frame):
        self.main_header = frame
        
    def assign_headline_frames(self,frames):
        self.headline_frames = frames
        
    def delete_frame_contents(self,frame):
        # delete all widgets inside a frame while preserving the frame itself
        for widget in frame.winfo_children():
            widget.destroy()
            
    def add_table_frame(self,name,frame):
        # Add the identifier of a frame to the state object so it can be cleared/destroyed later if needed
        self.table_frames[name] = frame
    
    def clear_all_tabs(self):
        for tab in self.tabs[1:]:
            self.delete_frame_contents(tab)
            
    def destroy_table_frame(self, frame):
        if frame in self.table_frames.keys():
            self.table_frames[frame].destroy()
        else: print("Frame " + frame + " was designated for destruction but could not be destroyed.")
    
    def set_name_stringvar(self,name):
        self.kname = name
    
    def write_headline_stats(self):
        kingdom = self.kingdom
        tabs = self.tabs
        headline_frames = self.headline_frames
        index = 0
        for tab in tabs:
            self.delete_frame_contents(headline_frames[index])
            level_label = tk.Label(headline_frames[index], text="Level: " + str(kingdom.level)) 
            level_label.grid(row=1, column=0)
            control_label = tk.Label(headline_frames[index], text="Control DC: " + str(kingdom.control_DC))
            control_label.grid(row=1, column=1,padx=10)            
            hexes_label = tk.Label(headline_frames[index], text="Claimed Hexes: " + str(len(kingdom.claimed_hexes))) 
            hexes_label.grid(row=1, column=2,padx=10)
            vsep1 = ttk.Separator(headline_frames[index],orient="vertical")
            vsep1.grid(row=1,column=3,sticky="nsew")
            ########################
            food_label = tk.Label(headline_frames[index], text="Food: " + str(kingdom.resources["food"][0]))
            food_label.grid(row=1, column=4, padx=10)
            food_capacity_label = tk.Label(headline_frames[index], text="Food Consumed/Turn: " + 
                                           str(kingdom.get_consumption()))
            food_capacity_label.grid(row=1, column=5, padx=10)
            food_turn_label = tk.Label(headline_frames[index], text="Food Gained/Turn: " + 
                                       str(kingdom.resources["food"][2]))
            food_turn_label.grid(row=1, column=6, padx=10)
            vsep2 = ttk.Separator(headline_frames[index],orient="vertical")
            vsep2.grid(row=1,column=7,sticky="nsew")
            ##############################
            resource_dice_label = tk.Label(headline_frames[index], text = "Base Resource Dice: " + 
                                           kingdom.get_base_resource_die_string())
            resource_dice_label.grid(row=1, column=8, padx=10)            
            resource_col = 9
            for resource in resources:
                resource_label = tk.Label(headline_frames[index],
                                          text=resource.title() + ": " + str(kingdom.resources[resource][0]))
                resource_label.grid(row=1,column=resource_col,padx=10)
                resource_col += 1
            vsep3 = ttk.Separator(headline_frames[index],orient="vertical")
            vsep3.grid(row=1,column=13,sticky="nsew")
            ########################
            unrest_label = tk.Label(headline_frames[index], text="Unrest: " + str(kingdom.unrest))
            unrest_label.grid(row=1, column=14, padx=10)            
            ruin_startcol=15
            for ruin in Ruins:
                ruin_label = tk.Label(headline_frames[index],text = ruin.title() + ": " + str(kingdom.ruins[ruin]))
                ruin_label.grid(row=1, column=ruin_startcol,padx=10)
                ruin_startcol += 1
            vsep4 = ttk.Separator(headline_frames[index],orient="vertical")
            vsep4.grid(row=1,column=19,sticky="nsew")
            index += 1