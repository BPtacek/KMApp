# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 22:52:21 2023

@author: dtbla
"""
class Event:
    def __init__(self,name="",dc_mod=0,skill="",etype="",text=""):
        self.name = name
        self.dc_mod = dc_mod
        self.etype = etype
        self.text = text
        
event_names = ["Archaeological Find","Assassination Attempt","Bandit Activity","Boomtown","Building Demand",
               "Crop Failure","Cult Activity","Diplomatic Overture","Discovery","Drug Den","Economic Surge",
               "Expansion Demand","Festive Invitation","Feud","Food Shortage","Food Surplus","Good Weather",
               "Inquisition","Justice Prevails","Land Rush","Local Disaster","Monster Activity","Natural Disaster",
               "Nature’s Blessing","New Subjects","Noblesse Oblige","Outstanding Success","Pilgrimage","Plague",
               "Political Calm","Public Scandal","Remarkable Treasure","Sacrifices","Sensational Crime","Squatters",
               "Undead Uprising","Unexpected Find","Vandals","Visiting Celebrity","Wealthy Immigrant"]

ArchFind = KEvent(name=event_names[0],dc_mod=0,skill="exploration",etype="beneficial")
AssAtt = KEvent(name=event_names[1],dc_mod=1,skill="intrigue",etype="dangerous")