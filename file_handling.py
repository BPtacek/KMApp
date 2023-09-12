# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:45:59 2023

@author: dtbla
"""
import tkinter
from tkinter import filedialog as fd
import json
from constants import *
# from buildings import *
from nethysparse import *

def read_json(kingdom):
    f = fd.askopenfile(filetypes=[("json files","*.json")])
    data = json.load(f)
    kingdom.reset()
    kingdom.set_name(data["name"])
    kingdom.set_unrest(data["unrest"])
    kingdom.set_ruins(data["ruins"])
    kingdom.set_level(data["level"])                      
    kingdom.set_attributes(data["attributes"])
    kingdom.set_skills(data["skills"])
    kingdom.set_advisors(data["advisors"])
    kingdom.set_relations(data["relations"])
    kingdom.set_RP(data["RP"])
    kingdom.set_resources(data["resources"])
    kingdom.set_xp(data["xp"])
    kingdom.set_work_camps(data["work_camps"])
    kingdom.set_capital(data["capital"])
    for i in data["claimed_hexes"]:
        kingdom.add_hex((i[0],i[1]))    
    for i in data["explored_hexes"]:
        kingdom.add_explored_hex((i[0],i[1]))
    for settlement in data["settlements"]:
        name = settlement["name"]
        location = (settlement["location"][0],settlement["location"][1])
        buildings = {}
        for (building,number) in settlement["buildings"].items():
            target = [i for i in Buildings if building == i.name]
            buildings[target[0]] = number
        kingdom.add_settlement(name,location,buildings)
    try:
        for coordinates in data["roads"]:
            kingdom.add_road(coordinates)
    except: kingdom.roads = []
    f.close()
    
def export_kingdom_as_file(kingdom, print_only=False):            
    file_name = kingdom.name + ".json"
    kingdom_data = kingdom.export_kingdom_data()
    if print_only:
        print(json.dumps(kingdom_data, indent=4))
        return
    with open(f"{file_name}", "w") as f:
        json.dump(kingdom_data, f, indent=4)