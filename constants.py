# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:37:47 2023

@author: dtbla
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:22:55 2023

@author: dtbla
"""
import random

########################################
### Important constants:

Kingdom_skills = {"agriculture": "stability", "arts": "culture", "boating": "economy", "defense": "stability",
                  "engineering": "stability", "exploration": "economy", "folklore": "culture", "industry": "economy",
                  "intrigue": "loyalty", "magic": "culture", "politics": "loyalty", "scholarship": "culture",
                  "statecraft": "loyalty", "trade": "economy", "warfare": "loyalty", "wilderness": "stability"}
# Kingdom_skills is a dictionary {skill:attribute} of all the kingdom skills and the associated kingdom attributes
Ruins = ["corruption", "crime", "decay", "strife"]
Advisors = {"ruler": "loyalty", "emissary": "loyalty", "general": "stability", "magister": "culture",
            "counselor": "culture", "treasurer": "economy", "viceroy": "economy", "warden": "stability"}
size_thresholds = {0: {"type":"Territory","rd size":4,"dc modifier":0,"storage":4}, 
                   9: {"type":"Province","rd size":6,"dc modifier":1,"storage":8}, 
                   24: {"type":"State","rd size":8,"dc modifier":2,"storage":12}, 
                   49: {"type":"Country","rd size":10,"dc modifier":3,"storage":16}, 
                   99: {"type":"Dominion","rd size":4,"dc modifier":4,"storage":20}}  
# Dict, no. claimed hexes corresponding to upper limit for indicated size penalty
control_DC_table = {1: 14, 2: 15, 3: 16, 4: 18, 5: 20, 6: 22, 7: 23, 8: 24, 9: 26, 10: 27, 11: 28, 12: 30, 13: 31,
                    14: 32,
                    15: 34, 16: 35, 17: 36, 18: 38, 19: 39, 20: 40}  # {Kingdom level:control DC}
leadership_status_bonuses = {1: 1, 8: 2,
                             16: 3}  # kingdom level and associated status bonus to skill checks for filling leadership
settlement_consumption_scaling = {1:1,2:2,4:5,6:10}  # {settlement size threshold : settlement consumption value}.
attributes = ["loyalty","stability","culture","economy"]
prof_dict = {0:"Untrained",1:"Trained",2:"Expert",3:"Master",4:"Legendary"}
resources_jobsites = {"lumber":"Logging Camps","stone":"Quarries","ore":"Mines","food":"Farms"}


# Settlment size is defined in numbers of filled blocks; each block has 4 lots.
# Each building in a settlement takes up a set number of lots.

###### End of important constants
#############################################

#################
### Utility functions:                  
def skills_for_attribute(attribute):
    # str -> list; return a list of all skills associated with a named attribute
    return [i for i in Kingdom_skills if Kingdom_skills[i] == attribute]


def d20():
    return random.randint(1, 20)


def d12():
    return random.randint(1, 12)


def d10():
    return random.randint(1, 10)


def d8():
    return random.randint(1, 8)


def d6():
    return random.randint(1, 6)


def d4():
    return random.randint(1, 4)
#### End of utility functions
#################
