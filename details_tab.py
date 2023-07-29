# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:12:05 2023

@author: dtbla
"""
from constants import *
import tkinter as tk
from tkinter import ttk

def draw_attribute_overview(state):
    kingdom = state.kingdom
    attribute_variables = state.attribute_variables
    skill_modifiers = state.skill_modifiers
    target_frame = state.tabs[0]
    attribute_table_startrow=38
    attribute_table_startcol = 0
    for attribute in attributes:
        attribute_frame = tk.Frame(target_frame,borderwidth=1,relief="groove")
        attribute_header = tk.Frame(attribute_frame)
        attribute_frame.grid(row = attribute_table_startrow, column = attribute_table_startcol)
        attribute_header.grid(row=0,column=0,columnspan=4)
        header_label = tk.Label(attribute_header, text = attribute.title() + ": ")
        header_value = tk.Label(attribute_header, textvariable=attribute_variables[attribute])
        header_label.grid(row=0,column=0,sticky="e")
        header_value.grid(row=0,column=1,sticky="w")        
        advisors_label = tk.Label(attribute_frame, text="Leaders")
        advisors_label.grid(row=2, column=0,columnspan=2)
        skills_label = tk.Label(attribute_frame, text = "Skill Modifiers")
        skills_label.grid(row=2, column=3,columnspan=2)
        advisor_row = 4
        for advisor in Advisors.keys():
            if Advisors[advisor] == attribute:
                advisor_label = tk.Label(attribute_frame, text=advisor.title() + ": ")
                advisor_label.grid(row = advisor_row, column=0, rowspan=2,sticky="ns")
                advisor_status = tk.Label(attribute_frame, text="Assigned")
                advisor_status.grid(row=advisor_row, column=1, rowspan=2,sticky="ns")
                advisor_row += 2
        skill_row = 4
        for skill in Kingdom_skills.keys():
            if Kingdom_skills[skill] == attribute:
                skill_label = tk.Label(attribute_frame, text = skill.title() + ": ")
                skill_value = tk.Label(attribute_frame, textvariable=skill_modifiers[skill])
                skill_label.grid(row=skill_row, column=3)
                skill_value.grid(row=skill_row,column=4)
                skill_row += 1
        for row in [1,3]:
            hsep = ttk.Separator(attribute_frame, orient="horizontal")
            hsep.grid(row=row, column=0, columnspan=5, sticky="ew")
        vsep = ttk.Separator(attribute_frame, orient="vertical")
        vsep.grid(row=1, column=2, rowspan=10, sticky="ns")
        attribute_table_startcol += 1
        
def increase_skill(skill,state):
    state.kingdom.increase_skill(skill)
    state.update_stringvars()

def reduce_skill(skill,state):
    state.kingdom.reduce_skill(skill)
    state.update_stringvars()
    
def increase_attribute(attribute,state):
    state.kingdom.increase_attribute(attribute)
    state.update_stringvars()

def reduce_attribute(attribute,state):
    state.kingdom.reduce_attribute(attribute)
    state.update_stringvars()
    
def draw_attribute_details(state):
    kingdom=state.kingdom
    attribute_variables=state.attribute_variables
    skill_modifiers=state.skill_modifiers
    proficiency_variables=state.proficiency_variables
    target_frame = state.tabs[1]
    # draw the detailed attributes/skills/leaders table in the Kingdom Details tab
    attribute_table_frame = tk.Frame(target_frame,borderwidth=1,relief="groove")
    attribute_table_header = tk.Label(attribute_table_frame,
                                      text="Kingdom Attributes, Skills, & Leaders",font=("Segoe UI",10,"bold"))    
    attribute_table_header.grid(row=0,column=0)
    attribute_table_frame.grid(row=5, column=0, rowspan=100,padx=10)
    state.add_table_frame("attribute details",attribute_table_frame)
    attribute_table_startrow=6
    attribute_table_startcol = 0
    state.update_stringvars()
    for attribute in attributes:
        attribute_frame = tk.Frame(attribute_table_frame,borderwidth=1,relief="groove")
        attribute_header = tk.Frame(attribute_frame)
        attribute_frame.grid(row = attribute_table_startrow, column = attribute_table_startcol, sticky="nsew")
        attribute_header.grid(row=0,column=0,columnspan=8)
        header_label = tk.Label(attribute_header, text = attribute.title() + ": ")
        header_value = tk.Label(attribute_header, textvariable=attribute_variables[attribute])
        attribute_up_button = tk.Button(attribute_header, text="^",
                                        command = lambda a=attribute,s=state: increase_attribute(a,s))
        attribute_down_button = tk.Button(attribute_header, text="v",
                                        command = lambda a=attribute,s=state: reduce_attribute(a,s))            
        header_label.grid(row=0,column=0,sticky="e")
        header_value.grid(row=0,column=1,sticky="w")        
        attribute_up_button.grid(row=0, column=2)
        attribute_down_button.grid(row=0, column=3)
        advisors_label = tk.Label(attribute_frame, text="Leaders")
        advisors_label.grid(row=2, column=0,columnspan=2)
        skills_label1 = tk.Label(attribute_frame, text = "Skill")
        skills_label1.grid(row=2, column=3)
        skills_label2 = tk.Label(attribute_frame, text = "Proficiency")
        skills_label2.grid(row=2, column=4)
        skills_label3 = tk.Label(attribute_frame, text = "Modifier")
        skills_label3.grid(row=2, column=5)
        advisor_row = 4
        for advisor in Advisors.keys():                
            if Advisors[advisor] == attribute:
                advisor_label = tk.Label(attribute_frame, text=advisor.title() + ": ", width=8)
                advisor_label.grid(row = advisor_row, column=0, rowspan=2,sticky="ew")
                advisor_status = tk.Label(attribute_frame, text="Assigned",width=8)
                advisor_status.grid(row=advisor_row, column=1, rowspan=2,sticky="ew")
                advisor_row += 2
        skill_row = 4
        for skill in Kingdom_skills.keys():                
            if Kingdom_skills[skill] == attribute:
                skill_label = tk.Label(attribute_frame, text = skill.title() + ": ")
                skill_value = tk.Label(attribute_frame, textvariable=skill_modifiers[skill])
                skill_up_button = tk.Button(attribute_frame, text="^",
                                            command = lambda k=skill,t=state: increase_skill(k,t))
                skill_down_button = tk.Button(attribute_frame, text="v",
                                            command = lambda k=skill,t=state: reduce_skill(k,t))   
                skill_label.grid(row=skill_row, column=3)
                proficiency_label = tk.Label(attribute_frame, textvariable=proficiency_variables[skill])
                proficiency_label.grid(row=skill_row, column=4)
                skill_value.grid(row=skill_row,column=5)
                skill_up_button.grid(row=skill_row, column=6)
                skill_down_button.grid(row=skill_row, column=7)
                skill_row += 1
        for row in [1,3]:
            hsep = ttk.Separator(attribute_frame, orient="horizontal")
            hsep.grid(row=row, column=0, columnspan=20, sticky="ew")
        vsep = ttk.Separator(attribute_frame, orient="vertical")
        vsep.grid(row=1, column=2, rowspan=10, sticky="ns")
        attribute_table_startrow += 15   
        
        
def draw_name_table(state):
    kingdom = state.kingdom
    kingdom_details = state.tabs[1]
    name_table_frame = tk.Frame(kingdom_details, borderwidth=1,relief="groove")
    name_table_frame.grid(row=5, column=2,padx=10,sticky="n")
    state.add_table_frame("name table",name_table_frame)
    current_var = tk.StringVar(name_table_frame,value=kingdom.name)
    name_label = tk.Label(name_table_frame,text = "Kingdom Name:")
    name_label.grid(row=0,column=0)
    current_name = tk.Label(name_table_frame,textvariable=current_var)
    current_name.grid(row=0,column=1)
    new_label = tk.Label(name_table_frame,text = "New Name: ")
    new_label.grid(row=1, column=0)
    new_name = tk.StringVar(name_table_frame,value="")
    name_box = tk.Entry(name_table_frame,textvariable=new_name)
    name_box.grid(row=1,column=1)
    def name_listener(event=None,namevar = new_name,cname=current_var,state=state): # both this and kingdom.increase(xp) need lots of input sanitization!
        change = name_box.get()
        kingdom.set_name(change)
        state.kname.set(change)
        namevar.set("")
        current_var.set(kingdom.name)
    name_box.bind("<Return>",name_listener)
    
def draw_level_table(state):
    # draw the level/XP/XP gain table in the Kingdom Details tab
    kingdom = state.kingdom
    kingdom_details = state.tabs[1]
    level_table_frame = tk.Frame(kingdom_details, borderwidth=1,relief="groove")
    level_table_frame.grid(row=6, column=2,padx=10,sticky="n")
    state.add_table_frame("level table",level_table_frame)
    header_frame = tk.Frame(level_table_frame)
    header_frame.grid(row=0, column = 0, columnspan=50)
    header = tk.Label(header_frame,text="Kingdom Level and XP",font=("Segoe UI",10,"bold"))
    header.grid(row=0, column=0, columnspan=50,padx=5)
    level_frame = tk.Frame(level_table_frame)
    level_frame.grid(row=1, column = 0, columnspan=50,sticky="w",padx=5)
    level_label = tk.Label(level_frame, text = "Kingdom Level: " + str(kingdom.level))
    level_label.grid(row=0, column=0,sticky="w")
    def increase_level(state):
        state.kingdom.increase_level()
        state.update_stringvars()
        state.write_headline_stats()
        draw_level_table(state)
    def reduce_level(state):
        state.kingdom.reduce_level()
        state.update_stringvars()
        state.write_headline_stats()
        draw_level_table(state)
    level_up_button = tk.Button(level_frame, text="^",
                                command = lambda st=state: increase_level(st))
    level_down_button = tk.Button(level_frame, text="v",
                                  command = lambda st=state: reduce_level(st))
    level_up_button.grid(row=0, column=1)
    level_down_button.grid(row=0, column=2)
    xp_frame = tk.Frame(level_table_frame)
    xp_label = tk.Label(xp_frame, text = "Kingdom XP: " + str(kingdom.xp) + "/1000")
    increase_xp = tk.Label(xp_frame, text = "Increase XP by:")
    add_xp = tk.StringVar(xp_frame, value="0")
    xp_entry = tk.Entry(xp_frame,width=6,textvariable=add_xp)
    def xp_listener(event=None): # both this and kingdom.increase(xp) need lots of input sanitization!
        xp_to_add = xp_entry.get()
        kingdom.increase_xp(xp_to_add)
        state.update_stringvars()
        state.write_headline_stats()
        draw_level_table(state)
    xp_entry.bind("<Return>",xp_listener)
    xp_label.grid(row=0, column=0,padx=5)        
    increase_xp.grid(row=0, column=1)
    xp_entry.grid(row=0, column=2)
    xp_frame.grid(row=2,column=0)        

def draw_resource_table(state):
    # draw the resources table in the Kingdom Details tab
    kingdom = state.kingdom
    kingdom_details = state.tabs[1]
    resource_table_frame = tk.Frame(kingdom_details, borderwidth=1,relief="groove")
    resource_table_frame.grid(row=7, column=2,sticky="n")
    state.add_table_frame("resource table",resource_table_frame)
    header_frame = tk.Frame(resource_table_frame)
    header_frame.grid(row=0, column = 0, columnspan=50)
    header = tk.Label(header_frame,text="Kingdom Resources",font=("Segoe UI",10,"bold"))
    header.grid(row=0, column=0, columnspan=50,padx=5)
    resource_frame = tk.Frame(resource_table_frame)
    resource_frame.grid(row=1, column=0)
    resource_name = tk.Label(resource_frame,text="Resource")
    resource_name.grid(row=0,column=0,padx=2)
    resource_value = tk.Label(resource_frame,text="Stored Amount")
    resource_value.grid(row=0,column=1,padx=2)
    capacity_label = tk.Label(resource_frame,text="Storage Capacity")
    capacity_label.grid(row=0,column=2,padx=2)
    gain_label = tk.Label(resource_frame,text="Gain Per Turn")
    gain_label.grid(row=0,column=3,padx=2)
    resource_startrow=1
    for resource in kingdom.resources.keys():
        name = tk.Label(resource_frame,text=resource.title())       
        name.grid(row=resource_startrow, column=0)
        current = tk.Label(resource_frame, text=str(kingdom.resources[resource][0]))
        current.grid(row=resource_startrow, column=1)
        capacity = tk.Label(resource_frame, text=str(kingdom.resources[resource][1]))
        capacity.grid(row=resource_startrow,column=2)
        gain = tk.Label(resource_frame,text=str(kingdom.resources[resource][2]))
        gain.grid(row=resource_startrow,column=3)
        resource_startrow += 1
        
def draw_unrest_table(state):
    # draw the unrest table in the Kingdom Details tab
    kingdom = state.kingdom
    kingdom_details = state.tabs[1]
    unrest_frame = tk.Frame(kingdom_details,borderwidth=1,relief="groove")
    unrest_frame.grid(row=8,column=2,sticky="n")
    state.add_table_frame("unrest table",unrest_frame)
    header_frame = tk.Frame(unrest_frame)
    header_frame.grid(row=0, column = 0, columnspan=50)
    header = tk.Label(header_frame,text="Unrest",font=("Segoe UI",10,"bold"))
    header.grid(row=0, column=0, columnspan=50,padx=5)
    main_frame = tk.Frame(unrest_frame)
    main_frame.grid(row=1,column=0)
    unrest_label = tk.Label(main_frame,text="Unrest: " + str(kingdom.unrest))
    unrest_penalty = tk.Label(main_frame, text="Unrest Penalty: " + str(-1 * kingdom.get_unrest_penalty()))
    unrest_label.grid(row=0,column=0)
    unrest_penalty.grid(row=1,column=0)
    change_unrest = tk.Label(main_frame,text="Increase/reduce unrest by:")
    change_unrest.grid(row=3,column=0)
    unrest_change = tk.StringVar(main_frame,value="0")
    unrest_entry = tk.Entry(main_frame,width=6,textvariable=unrest_change)
    unrest_entry.grid(row=3,column=1)
    def unrest_listener(event=None): # both this and kingdom.increase(xp) need lots of input sanitization!
        change = unrest_entry.get()
        kingdom.change_unrest(change)
        state.write_headline_stats()
        state.update_stringvars()
        draw_unrest_table(state)
    unrest_entry.bind("<Return>",unrest_listener)
    
def draw_ruins_table(state):
    # draw the ruins table in the Kingdom Details tab
    kingdom = state.kingdom
    kingdom_details = state.tabs[1]
    ruins_frame = tk.Frame(kingdom_details,borderwidth=1,relief="groove")
    ruins_frame.grid(row=9,column=2,sticky="n")
    state.add_table_frame("ruins table",ruins_frame)
    header_frame = tk.Frame(ruins_frame)
    header_frame.grid(row=0,column=0,columnspan=50)
    header = tk.Label(header_frame,text="Ruins",font=("Segoe UI",10,"bold"))
    header.grid(row=0,column=0)
    main_frame = tk.Frame(ruins_frame)
    main_frame.grid(row=1,column=1,columnspan=50)
    name_label = tk.Label(main_frame,text="Ruin")
    value_label = tk.Label(main_frame,text="Value")
    threshold_label = tk.Label(main_frame,text="Threshold")
    penalty_label = tk.Label(main_frame,text="Penalty")
    name_label.grid(row=0,column=0)
    value_label.grid(row=0,column=1)
    threshold_label.grid(row=0,column=2)
    penalty_label.grid(row=0,column=3)
    startrow=1
    for ruin in Ruins:
        name = tk.Label(main_frame,text=ruin.title())
        name.grid(row=startrow,column=0)
        value = tk.Label(main_frame,text=str(kingdom.ruins[ruin]))
        value.grid(row=startrow,column=1)
        threshold = tk.Label(main_frame,text="10")
        threshold.grid(row=startrow,column=2)
        penalty = tk.Label(main_frame,text="0")
        penalty.grid(row=startrow,column=3)
        startrow += 1
