# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:41:06 2023

@author: dtbla
"""
# this file contains data for every building in the game
from classes import *

Rubble = Building("Rubble", 1, 0, [0, 0, 0, 0, 0], ["None", 0, 0], 0, [0, 0, 0, 0, 0], False, False, {}, {})
Tenement = Building("Tenement", 1, 1, [1, 1, 0, 0, 0], ["Industry", 0, 14], 1, [1, 0, 0, 0, 0], False, True, {}, {})
Brewery = Building("Brewery", 1, 1, [6, 2, 0, 0, 0], ["Agriculture", 0, 15], 1, [0, 0, 0, 0, 0], False, False,
                   {"Establish Trade Agreement": 1}, {})
Cemetery = Building("Cemetery", 1, 1, [4, 1, 0, 0, 0], ["Folklore", 0, 15], 1, [0, 0, 0, 0, 0], False, False, {}, {})
GeneralStore = Building("General Store", 1, 1, [8, 1, 0, 0, 0], ["Trade", 0, 15], 1, [0, 0, 0, 0, 0], False, False,
                        {"Establish Trade Agreement": 1}, {})
Granary = Building("Granary", 1, 1, [12, 2, 0, 0, 0], ["Agriculture", 0, 15], 1, [0, 0, 0, 0, 0], False, False, {}, {})
Herbalist = Building("Herbalist", 1, 1, [10, 1, 0, 0, 0], ["Wilderness", 0, 15], 1, [0, 0, 0, 0, 0], False, False,
                     {"Provide Care": 1}, {})
Houses = Building("Houses", 1, 1, [3, 1, 0, 0, 0], ["Industry", 0, 15], 1, [0, 0, 0, 0, 0], False, True, {}, {})
Inn = Building("Inn", 1, 1, [10, 2, 0, 0, 0], ["Wilderness", 0, 15], 0, [0, 0, 0, 0, 0], False, True,
               {"Hire Adventurers": 1}, {})
Shrine = Building("Shrine", 1, 1, [8, 2, 1, 0, 0], ["Folklore", 0, 15], 0, [0, 0, 0, 0, 0], False, False,
                  {"Celebrate Holiday": 1}, {})
DiveTavern = Building("Tavern (Dive)", 1, 1, [12, 1, 0, 0, 0], ["Trade", 0, 15], 1, [0, 0, 1, 0, 0], False, False, {},
                      {})
WoodenWall = Building("Wall (Wooden)", 0, 1, [2, 4, 0, 0, 0], ["Defense", 0, 15], 1, [0, 0, 0, 0, 0], False, False, {},
                      {})
Bridge = Building("Bridge", 0, 2, [6, 1, 1, 0, 0], ["Engineering", 0, 16], 0, [0, 0, 0, 0, 0], False, False, {}, {})
Dump = Building("Dump", 1, 2, [4, 0, 0, 0, 0], ["Industry", 0, 16], 0, [0, 0, 0, 0, 0], False, False, {"Demolish": 1},
                {})
Jail = Building("Jail", 1, 2, [14, 4, 4, 2, 0], ["Defense", 0, 16], 0, [0, 0, -1, 0, 0], False, False,
                {"Quell Unrest (Intrigue)": 1}, {})
Library = Building("Library", 1, 2, [6, 4, 2, 0, 0], ["Scholarship", 1, 16], 0, [0, 0, 0, 0, 0], False, False,
                   {"Rest and Relax (Scholarship)": 1},
                   {"Recall Knowledge (Lore)": 1, "Research": 1, "Decipher Writing": 1})
Mill = Building("Mill", 1, 2, [6, 2, 1, 0, 0], ["Industry", 1, 16], 0, [0, 0, 0, 0, 0], True, False,
                {"Harvest Crops": 1}, {})
Orphanage = Building("Orphanage", 1, 2, [6, 2, 0, 0, 0], ["Industry", 0, 16], 1, [0, 0, 0, 0, 0], False, True, {}, {})
TownHall = Building("Town Hall", 2, 2, [22, 4, 4, 0, 0], ["Defense", 1, 16], 1, [0, 0, 0, 0, 0], False, False, {}, {})
AlchemyLab = Building("Alchemy Lab", 1, 3, [18, 0, 5, 2, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                      {"Demolish": 1}, {"Identify (Alchemical)": 1})
PopularTavern = Building("Tavern (Popular)", 1, 3, [24, 6, 2, 0, 0], ["Trade", 2, 18], 2, [0, 0, 0, 0, 0], False, False,
                         {"Hire Adventurers": 1, "Rest and Relax (Trade)": 1},
                         {"Earn Income (Performance)": 1, "Gather Information": 1})
Barracks = Building("Barracks", 1, 3, [6, 2, 1, 0, 0], ["Defense", 0, 18], 1, [0, 0, 0, 0, 0], False, True,
                    {"Garrison Army": 1, "Recover Army": 1, "Recruit Army": 1}, {})
FestivalHall = Building("Festival Hall", 1, 3, [7, 3, 0, 0, 0], ["Arts", 0, 18], 0, [0, 0, 0, 0, 0], False, False,
                        {"Celebrate Holiday": 1}, {})
Foundry = Building("Foundry", 2, 3, [16, 5, 2, 3, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                   {"Establish Work Site (Mine)": 1}, {})
Keep = Building("Keep", 2, 3, [32, 8, 8, 0, 0], ["Defense", 1, 18], 1, [0, 0, 0, 0, 0], False, False,
                {"Deploy Army": 1, "Garrison Army": 1, "Train Army": 1}, {})
Lumberyard = Building("Lumber Yard", 2, 3, [16, 5, 0, 1, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                      {"Establish Work Site (Lumber Camp)": 1}, {})
Monument = Building("Monument", 1, 3, [6, 0, 1, 0, 0], ["Arts", 1, 18], 1, [1, 0, 0, 0, 0], False, False, {}, {})
Park = Building("Park", 1, 3, [6, 0, 1, 0, 0], ["Wilderness", 0, 18], 1, [0, 0, 0, 0, 0], False, False,
                {"Rest and Relax (Wilderness)": 1}, {})
Pier = Building("Pier", 1, 3, [16, 2, 0, 0, 0], ["Boating", 0, 18], 0, [0, 0, 0, 0, 0], False, False, {"Go Fishing": 1},
                {})
Smithy = Building("Smithy", 1, 3, [8, 2, 1, 0, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                  {"Trade Commodities": 1, "Outfit Army": 1}, {"Crafting": 1})
Stable = Building("Stable", 1, 3, [10, 2, 0, 0, 0], ["Wilderness", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                  {"Establish Trade Agreement": 1}, {})
Stockyard = Building("Stockyard", 4, 3, [20, 4, 0, 0, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], True, False,
                     {"Gather Livestock": 1}, {})
Stonemason = Building("Stonemason", 2, 3, [16, 2, 0, 0, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                      {"Establish Work Site (Quarry)": 1}, {})
Tannery = Building("Tannery", 1, 3, [6, 2, 0, 0, 0], ["Industry", 1, 18], 0, [0, 0, 0, 0, 0], False, False,
                   {"Trade Commodities": 1}, {})
TradeShop = Building("Trade Shop", 1, 3, [10, 2, 0, 0, 0], ["Trade", 2, 18], 0, [0, 0, 0, 0, 0], False, False,
                     {"Purchase Commodities": 1}, {})
Watchtower = Building("Watchtower", 1, 3, [12, 4, 4, 0, 0], ["Defense", 1, 18], 1, [0, 0, 0, 0, 0], False, False,
                      {"Resolve Events": 1}, {})
Marketplace = Building("Marketplace", 2, 4, [48, 4, 0, 0, 0], ["Trade", 1, 19], 0, [0, 0, 0, 0, 0], False, True,
                       {"Establish Trade Agreement": 1}, {})
Pavedstreets = Building("Paved Streets", 0, 4, [12, 0, 6, 0, 0], ["Industry", 1, 19], 0, [0, 0, 0, 0, 0], False, False,
                        {}, {})
Specialartisan = Building("Specialized Artisan", 1, 4, [10, 4, 0, 0, 1], ["Trade", 2, 19], 0, [0, 0, 0, 0, 0], False,
                          False,
                          {"Craft Luxuries": 1}, {"Crafting": 1})
Arcanist = Building("Arcanist's Tower", 1, 5, [30, 0, 6, 0, 0], ["Magic", 1, 20], 0, [0, 0, 0, 0, 0], False, False,
                    {"Quell Unrest (Magic)": 1}, {"Borrow A Spell (Arcane)": 1, "Learn A Spell": 1})
Bank = Building("Bank", 1, 5, [28, 0, 6, 4, 0], ["Trade", 1, 20], 0, [0, 0, 0, 0, 0], False, False, {"Tap Treasury": 1},
                {})
Garrison = Building("Garrison", 2, 5, [28, 6, 3, 0, 0], ["Warfare", 1, 20], 1, [0, 0, 0, 0, 0], False, True,
                    {"Outfit Army": 1, "Train Army": 1}, {})
Guildhall = Building("Guildhall", 2, 5, [34, 8, 0, 0, 0], ["Trade", 2, 20], 0, [0, 0, 0, 0, 0], False, False, {}, {})
Magiclamps = Building("Magical Street Lamps", 0, 5, [20, 0, 0, 0, 0], ["Magic", 2, 20], 0, [0, 0, 1, 0, 0], False,
                      False, {}, {})
Mansion = Building("Mansion", 1, 5, [10, 6, 3, 0, 6], ["Industry", 1, 20], 0, [0, 0, 0, 0, 0], False, True,
                   {"Improve Lifestyle": 1}, {})
Museum = Building("Museum", 2, 5, [30, 6, 2, 0, 0], ["Exploration", 1, 20], 0, [0, 0, 0, 0, 0], False, False,
                  {"Rest and Relax (Arts)": 1}, {})
Sacredgrove = Building("Sacred Grove", 1, 5, [36, 0, 0, 0, 0], ["Wilderness", 1, 20], 0, [0, 0, 0, 0, 0], False, False,
                       {"Quell Unrest (Folklore)": 1}, {})

Buildings = (Rubble, Tenement, Brewery, Cemetery, GeneralStore, Granary, Herbalist, Houses, Inn, Shrine, DiveTavern,
             WoodenWall, Bridge, Dump, Jail, Library, Mill, Orphanage, TownHall, AlchemyLab, PopularTavern, Barracks,
             Foundry, FestivalHall, Keep, Lumberyard, Monument, Park, Pier, Smithy, Stable, Stockyard, Stonemason,
             Tannery, TradeShop, Watchtower, Marketplace, Pavedstreets, Specialartisan, Arcanist, Bank, Garrison,
             Guildhall, Magiclamps, Mansion, Museum, Sacredgrove)
