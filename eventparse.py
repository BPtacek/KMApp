# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 17:04:34 2023

@author: dtbla
"""
import re
from classes import *

f = open("Data/nethysevents.txt", "r",encoding="utf8")
start_string2 = f.read()
f.close()
titlestring = "<h2 class=\"title\">"
split_string = start_string2.split(titlestring)[1:]

string_list=[]
second_splitter = "<br />"
for entry in split_string:
    q = entry.split(second_splitter)
    string_list.append(q)

event_list = {}
for event in string_list:
    for line in event:
        if "<a href=\"KMEvents" in line:
            n = re.search("KMEvents.aspx\?ID=\d?\d?\d\">([^<]*)</a>",line)
            name = n.group(1)
            dc_mod = re.search("Event\s([^<]*)</span>",line)
            event_list[name] = {"DC modifier":dc_mod.group(1)}
            traits = re.findall("Traits.aspx[^>]*>([^<]*)</a>",line)
            event_list[name]["Traits"] = traits
        if "Skills" not in event_list[name].keys():
            event_list[name]["Skills"] = []
        s = re.search("Skills.aspx[^>]*>([^<]*)</a>",line)
        if s and s.group(1) not in event_list[name]["Skills"]: 
            event_list[name]["Skills"].append(s.group(1))
        if "Location" in line:
            loc = re.search("</b>\s(.*)",line)
            location = re.sub("<[^>]*>","",loc.group(1))
            event_list[name]["Location"] = location
        if (not "<" in line) and (not ">" in line) and line != "":
            stripped_line = re.sub("<[^>]*>","",line)
            event_list[name]["Description"] = stripped_line
        if "<b>Critical Success</b>" in line:
            cs = re.search("</b>\s(.*)",line)
            crit_text = re.sub("<[^>]*>","",cs.group(1))
            event_list[name]["Critical Success"] = crit_text
        if "<b>Success</b>" in line:
            s = re.search("</b>\s(.*)",line)
            succ_text = re.sub("<[^>]*>","",s.group(1))
            event_list[name]["Success"] = succ_text
        if "<b>Failure</b>" in line:
            fail = re.search("</b>\s(.*)",line)
            fail_text = re.sub("<[^>]*>","",fail.group(1))
            event_list[name]["Failure"] = fail_text
        if "Critical Failure" in line:
            cf = re.search("</b>\s(.*)",line)
            cf_text = re.sub("<[^>]*>","",cf.group(1))
            if "<b>Resolution</b>" in line:
                cf_text2 = cf_text.split("Resolution")
                event_list[name]["Critical Failure"] = cf_text2[0]
                if len(cf_text) >1:
                    event_list[name]["Resolution"] = cf_text2[1]                
            else:                
                event_list[name]["Critical Failure"] = cf_text
                event_list[name]["Resolution"] = ""
        if "Special" not in event_list[name].keys(): 
            event_list[name]["Special"] = ""
        if "<b>Special</b>" in line:
            spec = re.search("<b>Special</b>\s(.*)",line)
            spec2 = re.sub("<[^>]*>","",spec.group(1))
            event_list[name]["Special"] = spec2
            
def event_classifier():
    for skill in Kingdom_skills:
        skill = skill.title()
        print(skill.upper())
        print("Dangerous Events:")
        for (event_name,event_dict) in event_list.items():        
            if skill in event_dict["Skills"] and "Dangerous" in event_dict["Traits"]:
                print(" * " + event_name)
        print("------")
        print("Beneficial Events")
        for (event_name,event_dict) in event_list.items():        
            if skill in event_dict["Skills"] and "Beneficial" in event_dict["Traits"]:
                print(" * " + event_name)    
        print("==========================")