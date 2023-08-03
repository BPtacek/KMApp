# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 09:44:15 2023

@author: dtbla
"""
import re

f = open("nethysbuildings.txt", "r")
# print(f.read())

titlestring = "<h2 class=\"title\">"

start_string = f.read()
f.close()
split_string = start_string.split(titlestring)[1:]

string_list=[]
second_splitter = "<br />"
for entry in split_string:
    q = entry.split(second_splitter)
    string_list.append(q)

buildings_list = {}
for building in string_list:        
    for line in building:
        if "<a href" in line[:10]:            
            temp_name = re.search("\>([\w\s\'\,-]*)\<",line)
            name = temp_name.group(1)
            temp_level = re.search("Structure\s(\d?\d)<",line)
            level = temp_level.group(1)
            buildings_list[name] = {"level":level}
        if "Traits" in line and "Effects" not in line:
            traits = re.findall("Traits\.aspx\?ID=\d?\d?\d\">([A-Z][\w]*)",line)
            if "Traits" in buildings_list[name].keys():
                buildings_list[name]["Traits"] += traits
            else: buildings_list[name]["Traits"] = traits
        if "<hr /><b>" in line:
            temp_desc = re.search("(.*)<hr",line)
            description = str(temp_desc.groups(1))
            description2 = re.sub("<[^>]*>","",description)
            description3 = re.sub("â€”"," ",description2)
            buildings_list[name]["Description"] = str(description3)[2:-3]
        if "Lots</b>" in line:
            q = re.findall("Lots</b>\s([\d])",line)
            if q == []: lots = 0
            else: lots = q[0]
            buildings_list[name]["Lots"] = lots
        if "<b>Cost</b>" in line:
            rp = re.findall("(\d?\d)\sRP",line)
            if rp == []: buildings_list[name]["RP"] = 0
            else: buildings_list[name]["RP"] = rp[0]
            lumber = re.findall("(\d?\d)\sLumber",line)
            if lumber == []: buildings_list[name]["Lumber"] = 0
            else: buildings_list[name]["Lumber"] = lumber[0]
            stone = re.findall("(\d?\d)\sStone",line)
            if stone == []: buildings_list[name]["Stone"] = 0
            else: buildings_list[name]["Stone"] = stone[0]
            ore = re.findall("(\d?\d)\sOre",line)
            if ore == []: buildings_list[name]["Ore"] = 0
            else: buildings_list[name]["Ore"] = ore[0]
            luxuries = re.findall("(\d?\d)\sLuxuries",line)
            if luxuries == []: buildings_list[name]["Luxuries"] = 0
            else: buildings_list[name]["Luxuries"] = luxuries[0]
        if "Skills.aspx" in line and "Effects" not in line:
            skill = re.search(">(\w*)</a>",line)
            if not skill: buildings_list[name]["Skill"] = "None"
            else: buildings_list[name]["Skill"] = skill.group(1)
            if "master" in line: buildings_list[name]["Proficiency"] = "Master"
            elif "expert" in line: buildings_list[name]["Proficiency"] = "Expert"
            elif "trained" in line: buildings_list[name]["Proficiency"] = "Trained"
            else: buildings_list[name]["Proficiency"] = "Untrained"
            dc = re.search("DC\s(\d?\d)",line)
            if not dc: buildings_list[name]["DC"] = 0
            else: buildings_list[name]["DC"] = dc.group(1)
        if "Effects" in line or "Item Bonus" in line:
            unrest = re.search("Unrest\sby\s([^\.^\s]*)[\.\s]",line)
            if unrest: buildings_list[name]["Unrest Reduction"] = unrest.group(1)
            else: buildings_list[name]["Unrest Reduction"] = 0
        if "Unrest Reduction" not in buildings_list[name].keys(): buildings_list[name]["Unrest Reduction"] = 0
        consumption = re.search("Consumption by",line)
        if consumption: buildings_list[name]["Consumption Reduction"] = 1
        else: buildings_list[name]["Consumption Reduction"] = 0
        if "<b>Item Bonus</b>" in line:
            bonus = re.findall("b>\s(\+\d)\s\w*",line)
            skills = re.findall("ID=\d[\d?]*\">([A-Z][\w\s]*)</a>",line)
            buildings_list[name]["Item Bonus"] = bonus[0] if bonus != [] else "None"
            buildings_list[name]["Bonused Skills"] = skills
        if "Item Bonus" not in buildings_list[name].keys():
            buildings_list[name]["Item Bonus"] = "None"
            buildings_list[name]["Bonused Skills"] = "None"
        if "Crime" not in buildings_list[name].keys(): buildings_list[name]["Crime"] = 0
        if "Any Ruin" not in buildings_list[name].keys(): buildings_list[name]["Any Ruin"] = 0
        if "<b>Ruin</b>" in line and "Crime" in line: buildings_list[name]["Crime"] = 1
        elif "<b>Ruin</b>" in line and "Crime" not in line: buildings_list[name]["Any Ruin"] = 1
        elif "reduce one Ruin" in line: buildings_list[name]["Any Ruin"] = -1
        elif "increase Crime" in line: buildings_list[name]["Crime"] = 1
        elif "reduce Crime" in line: buildings_list[name]["Crime"] = -1
        if "Upgrade From" not in buildings_list[name].keys(): buildings_list[name]["Upgrade From"] = "None"
        if "Upgrade To" not in buildings_list[name].keys(): buildings_list[name]["Upgrade To"] = "None"
        if "Upgrade From" in line:
            upgrade_from = re.search("ID=\d?\d?\d\">([A-Z][\w\s,]*)</u>",line)
            buildings_list[name]["Upgrade From"] = upgrade_from.group(1)
        if "Upgrade To" in line:
            upgrade_to = re.findall("ID=\d?\d?\d\">([A-Z][\w\s,]*)</u>",line)
            buildings_list[name]["Upgrade To"] = upgrade_to
        if "Effects" in line:
            t = re.search("</b>(.*)",line)
            te = str(t.group(1))
            effects = re.sub("<[^>]*>","",te)
            buildings_list[name]["Effects"] = effects[1:]
        if "Effective Level" not in buildings_list[name].keys(): buildings_list[name]["Effective Level"] = {}
        if "reduces its effective level" in line: buildings_list[name]["Effective Level"]["Base"] = 2
        if "Treat the settlement's level" in line:
            tradition_present = False
            for tradition in ["arcane","primal","divine","luxury"]:
                if tradition in line:
                    tradition_present = True
                    buildings_list[name]["Effective Level"][tradition.title()] = 1
                if not tradition_present: buildings_list[name]["Effective Level"]["General"] = 1
        