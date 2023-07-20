# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:40:22 2023

@author: dtbla
"""

from constants import *


class Kingdom:
    def __init__(self, name, claimed_hexes, level, unrest, ruins, settlements, attributes, skills, advisors, relations,
                 RP, resources,xp):
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
        num_hexes = len(self.claimed_hexes)
        if num_hexes == 0:
            return 0        
        else:
            return max([j["dc modifier"] for (i, j) in size_thresholds.items() if i < num_hexes])

    def get_modifier(self, skill):
        # String -> Int, get the modifier (attribute + proficiency + building item + ruler circumstance) for the named skill
        skill_attribute = Kingdom_skills[skill]  # find the attribute corresponding to the named skill
        leadership_bonus_size = max(
            {leadership_status_bonuses[i] for i in leadership_status_bonuses.keys() if i < self.level})
        relevant_advisors = {i: j for (i, j) in Advisors.items() if Advisors[i] == skill_attribute}
        relevant_role_filled = True in [self.advisors[i] == "filled" for i in relevant_advisors.keys()]
        level_multiplier = self.level * (self.get_skill(skill) != 0)  # Int * Bool
        proficiency_bonus = 2 * self.get_skill(skill)
        attribute_bonus = (self.get_attribute(Kingdom_skills[skill]) - 10) // 2
        leadership_bonus = leadership_bonus_size * relevant_role_filled  # Int * Bool        
        return level_multiplier + proficiency_bonus + attribute_bonus + leadership_bonus

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
        data = self.__dict__
        kingdom_settlements = []
        tmp = {}
        for settlement in data["settlements"]:
            readable_settlement = settlement.__dict__
            if readable_settlement.get("buildings", False):
                for building in readable_settlement.get("buildings"):
                    tmp[building.name] = readable_settlement.get("buildings").get(building)
                readable_settlement["buildings"] = tmp
                tmp = {}
            kingdom_settlements.append(readable_settlement)
        data["settlements"] = kingdom_settlements
        return data 
    

class Settlement:
    def __init__(self, name, location, level, buildings):
        self.name = name  # String, settlement name
        self.location = location  # tuple (Int, Int) of grid coordinates specifying settlement's location
        self.level = level  # Int, settlement level
        self.buildings = buildings  # dictionary {Building:Int} of Building objects and number in settlement
        self.occupied_lots = sum(buildings[i] * i.lots for i in buildings)  # Int, number of lots occupied
        self.occupied_blocks = (self.occupied_lots // 4) + (self.occupied_lots % 4 > 0)  # number of blocks occupied

    def add_building(self, new_building):
        self.buildings[new_building] = self.buildings.get(new_building, 0) + 1
        self.occupied_lots += new_building.lots
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
        return min([a[i] for i in a.keys() if a[i] >= self.occupied_blocks]) - sum(consumption_reducers.values())

    def is_overcrowded(self):
        # self -> Bool, check if settlement has at least as many residential buildings as occupied blocks
        residences = {i: j for (i, j) in self.buildings.items() if
                      i.residential}  # types & numbers of residential buildings in settlement
        total_residences = sum(residences.values())  # total no. residential buildings in settlement
        return total_residences < self.occupied_blocks


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
