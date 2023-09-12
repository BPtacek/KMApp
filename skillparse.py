# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 20:21:54 2023

@author: dtbla
"""
import re
from classes import *
from constants import *

def gen_parser(input_file_name):    
    activity_dict = {}
    f = open(input_file_name, "r",encoding="utf8")    
    file_content = f.read()
    f.close()
    titlestring = "h1 class=\"title\">"
    first_split = file_content.split(titlestring)
    raw_activities = [i for i in first_split if "<a href=\"Skills" in i[0:20]]
    for raw_activity in raw_activities:
        find_name = re.search("General=true\">([^\(]*)\s\(",raw_activity)
        if find_name:
            name = find_name.group(1)
            activity_dict[name] = {}
            skills = re.findall("Skills.aspx\?ID=\d\d?\">([^<]*)</a>",raw_activity)
            activity_dict[name]["Skills"] = skills
            traits = re.findall("Traits.aspx\?ID=\d\d?\d?\">([^<]*)</a>",raw_activity)
            activity_dict[name]["Traits"] = traits
            reqs = re.search("Requirements</b>\s([^<]*)<hr",raw_activity)
            if reqs:
                activity_dict[name]["Requirements"] = reqs.group(1)
            desc = re.search("<hr\s/>(.*)<br\s/><b>Critical\sSuccess",raw_activity)
            if desc:
                description = re.sub("<[^>]*>","",desc.group(1))
                activity_dict[name]["Description"] = description
            else:
                if "Description" not in activity_dict[name].keys():
                    desc = re.search("<hr\s/>([^<]*)<br\s/>",raw_activity)
                    if desc:
                        activity_dict[name]["Description"] = desc.group(1)
            crit_success = re.search("<b>Critical\sSuccess</b>\s([^<]*)<br />",raw_activity)
            if crit_success:
                activity_dict[name]["Critical Success"] = crit_success.group(1)
            success = re.search("<b>Success</b>\s([^<]*)<br />",raw_activity)
            if success:
                activity_dict[name]["Success"] = success.group(1)
            failure = re.search("<b>Failure</b>\s([^<]*)<br />",raw_activity)
            if failure:
                activity_dict[name]["Failure"] = failure.group(1)
            crit_fail = re.search("<b>Critical\sFailure</b>\s([^<]*)<b",raw_activity)
            if crit_fail:
                activity_dict[name]["Critical Failure"] = crit_fail.group(1)
            special = re.search("<b>Special</b>\s([^<]*)<br",raw_activity)
            if special:
                activity_dict[name]["Special"] = special.group(1)
    return activity_dict

general_activities = gen_parser("Data/genskills.txt")

def skill_parser(input_file_name):    
    activity_dict = {}
    f = open(input_file_name, "r",encoding="utf8")    
    file_content = f.read()
    f.close()
    titlestring = "h1 class=\"title\">"
    first_split = file_content.split(titlestring)
    skill_entry = [i for i in first_split if "<a href=\"Skills" in i[0:20]]
    skill = re.search("Skills.aspx\?ID=\d\d?\">([^\(]*)\s\(",skill_entry[0])
    if skill:
        skill_name = skill.group(1)   
        activity_list = [i for i in first_split if "<h2 class=\"title\"><a href=\"Actions" in i[0:100]]
        if activity_list != []:
            activities = []
            for entry in activity_list:
                temp_activities = entry.split("<h2 class=\"title\">")
                activities += temp_activities
            for activity in activities:
                find_name = re.search("Actions.aspx\?ID=[\d]*\">([^<]*)</a>",activity)
                if find_name:
                    name = find_name.group(1)
                    activity_dict[name] = {}
                    activity_dict[name]["Skills"] = [skill_name]
                    traits = re.findall("Traits.aspx\?ID=\d\d?\d?\">([^<]*)</a>",activity)
                    activity_dict[name]["Traits"] = traits
                    reqs = re.search("Requirements</b>\s([^<]*)<hr",activity)
                    if reqs:
                        activity_dict[name]["Requirements"] = reqs.group(1)
                    desc = re.search("<hr\s/>(.*)<br\s/><b>Critical\sSuccess",activity)
                    if desc:
                        description = re.sub("<[^>]*>","",desc.group(1))
                        activity_dict[name]["Description"] = description
                    else:
                        if "Description" not in activity_dict[name].keys():
                            desc = re.search("<hr\s/>([^<]*)<br\s/>",activity)
                            if desc:
                                activity_dict[name]["Description"] = desc.group(1)
                    # desc = re.search("<hr />([^<]*)<br />",activity)
                    # if desc:
                    #     activity_dict[name]["Description"] = desc.group(1)
                    crit_success = re.search("<b>Critical\sSuccess</b>\s([^<]*)<br />",activity)
                    if crit_success:
                        activity_dict[name]["Critical Success"] = crit_success.group(1)
                    success = re.search("<b>Success</b>\s([^<]*)<br />",activity)
                    if success:
                        activity_dict[name]["Success"] = success.group(1)
                    failure = re.search("<b>Failure</b>\s([^<]*)<br />",activity)
                    if failure:
                        activity_dict[name]["Failure"] = failure.group(1)
                    crit_fail = re.search("<b>Critical\sFailure</b>\s([^<]*)<",activity)
                    if crit_fail:
                        activity_dict[name]["Critical Failure"] = crit_fail.group(1)
                    else:
                        crit_fail = re.search("<b>Critical\sFailure</b>\s([^<]*)",activity)
                        if crit_fail: activity_dict[name]["Critical Failure"] = crit_fail.group(1)
                    special = re.search("<b>Special</b>\s([^<]*)<br",activity)
                    if special:
                        activity_dict[name]["Special"] = special.group(1)
    return activity_dict

for i in range(1,17):
    filename = "Data/skill" + str(i) + ".txt"
    new_entries = skill_parser(filename)
    general_activities.update(new_entries)

general_activities["Claim Hex"]["Skills"] += ["Magic","Intrigue"]
general_activities["Focused Attention"]["Critical Success"] = "You grant another leader a +2 circumstance bonus on one kingdom check using the skill that you rolled."
general_activities["Focused Attention"]["Success"] = "You grant another leader a +2 circumstance bonus on one kingdom check using the skill that you rolled."
general_activities["Focused Attention"]["Failure"] = "You fail to provide effective aid but your efforts do no harm either."
general_activities["Focused Attention"]["Critical Failure"] = "You fail to provide effective aid but your efforts do no harm either."
general_activities["Focused Attention"]["Skills"] = [i.title() for i in Kingdom_skills.keys()]
general_activities["Build Structure"]["Skills"] = [i.title() for i in Kingdom_skills.keys()]
general_activities["Collect Taxes"]["Special"] = "If you don’t attempt to Collect Taxes in a kingdom turn, you can instead attempt a DC 11 flat check; on a success, reduce Unrest by 1."
############### Adding Summaries##################
general_activities["Abandon Hex"]["Summary"] = "Remove one hex from your kingdom."
general_activities["Build Structure"]["Summary"] = "Build a structure in one of your settlements."
general_activities["Claim Hex"]["Summary"] = "Add a hex to your kingdom."
general_activities["Clear Hex"]["Summary"] = "Remove a hazard or undesired terrain feature from a claimed hex."
general_activities["Establish Settlement"]["Summary"] = "Create a new settlement in a claimed hex."
general_activities["Establish Trade Agreement"]["Summary"] = "Enable trade with a neighbouring group or kingdom."
general_activities["Focused Attention"]["Summary"] = "Give another leader a bonus on a future kingdom check."
general_activities["New Leadership"]["Summary"] = "Install a new leader in a vacant kingdom leadership slot."
general_activities["Pledge of Fealty"]["Summary"] = "Add an existing settlement or kingdom to your kingdom."
general_activities["Quell Unrest"]["Summary"] = "Reduce Unrest."
general_activities["Repair Reputation"]["Summary"] = "Attempt to reduce one Ruin using Arts for Corruption, Engineering for Decay, Intrigue for Strife, or Trade for Crime."
general_activities["Rest and Relax"]["Summary"] = "Attempt to reduce Unrest."
general_activities["Establish Work Site"]["Summary"] = "Create a work camp to generate Lumber, Stone, or Ore."
general_activities["Hire Adventurers"]["Summary"] = "Stop an ongoing Event or gain a bonus on your next attempt to stop it."
general_activities["Celebrate Holiday"]["Summary"] = "Gain a bonus to future Loyalty checks."
general_activities["Trade Commodities"]["Summary"] = "Exchange Commodities now for RP next turn."
general_activities["Infiltration"]["Summary"] = "Gather intel on a hex or reduce Unrest."
general_activities["Supernatural Solution"]["Summary"] = "Reroll one future kingdom skill check using Magic instead of the initial skill."
general_activities["Improve Lifestyle"]["Summary"] = "Gain a bonus on future Culture checks."
general_activities["Harvest Crops"]["Summary"] = "Gain Food."
general_activities["Craft Luxuries"]["Summary"] = "Spend RP to gain Luxuries."
general_activities["Go Fishing"]["Summary"] = "Gain Food."
general_activities["Fortify Hex"]["Summary"] = "Build a fort in a claimed hex outside a settlement."
general_activities["Provide Care"]["Summary"] = "Reduce Unrest."
general_activities["Build Roads"]["Summary"] = "Build roads in a claimed hex."
general_activities["Demolish"]["Summary"] = "Destroy a building in one of your settlements."
general_activities["Creative Solution"]["Summary"] = "Reroll one future kingdom check with a +2 bonus."
general_activities["Tap Treasury"]["Summary"] = "Gain gold."
general_activities["Capital Investment"]["Summary"] = "Exchange gold for RP or undo Tap Treasury."
general_activities["Manage Trade Agreements"]["Summary"] = "Spend RP to gain RP and/or Commodities."
general_activities["Purchase Commodities"]["Summary"] = "Exchange RP for Commodities."
general_activities["Gather Livestock"]["Summary"] = "Gain Food."
general_activities["Create a Masterpiece"]["Summary"] = "Attempt to gain Fame or Infamy."
general_activities["Irrigation"]["Summary"] = "Add the river or lake terrain feature to a hex without it."
general_activities["Relocate Capital"]["Summary"] = "Move the Kingdom's capital to a new settlement."
general_activities["Clandestine Business"]["Summary"] = "Gain RP and/or Luxuries at the risk of raising Unrest."
general_activities["Prognostication"]["Summary"] = "Gain a bonus to resolve random Events this turn."
general_activities["Request Foreign Aid"]["Summary"] = "Gain RP and/or bonuses to future Kingdom checks."
general_activities["Send Diplomatic Envoy"]["Summary"] = "Establish diplomatic relationships with another group."
general_activities["Collect Taxes"]["Summary"] = "Boost Economy checks or try to reduce Unrest."
general_activities["Establish Farmland"]["Summary"] = "Build farms in a claimed hex."
######################################
for (i,j) in general_activities.items():
    j["Reduce Unrest"] = False
    if i in ["Quell Unrest","Rest and Relax","Fortify Hex","Provide Care","Infiltration",
             "Build Structure","Collect Taxes"]:
        j["Reduce Unrest"] = True
    j["Reduce Ruins"] = False
    if i in ["Repair Reputation","Infiltration","Provide Care"]:
        j["Reduce Ruins"] = True
    j["Gain RP"] = False
    if i in ["Request Foreign Aid","Manage Trade Agreements","Trade Commodities","Capital Investment",
             "Clandestine Business","Create a Masterpiece"]:
        j["Gain RP"] = True
    j["Gain Commodities"] = False
    if i in ["Purchase Commodities","Establish Work Site","Craft Luxuries","Manage Trade Agreements",
             "Clandestine Business"]:
        j["Gain Commodities"] = True
    j["Gain Food"] = False
    if i in ["Go Fishing","Harvest Crops","Gather Livestock","Establish Farmland"]:
        j["Gain Food"] = True