# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:46:48 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
# from buildings import *
from nethysparse import *
from constants import *

def settlement_type(state,ob):
    """Int -> String. Take settlement's level and number of occupied blocks, return its text classification"""
    settlement_types = {"Village":[1,1],"Town":[3,2],"City":[9,5],"Metropolis":[15,10]}
    kingdom = state.kingdom
    level = kingdom.level
    # {Settlement_type: [level threshold, occupied blocks threshold]}
    classification = "Village"
    reference_level = 0
    for i in settlement_types.keys():
        level_threshold = settlement_types[i][0]
        block_threshold = settlement_types[i][1]
        if level >= level_threshold and ob >= block_threshold and level >= reference_level:
            reference_level = level_threshold
            classification = i
    return classification

def draw_buildings_and_settlements_tables(state):
    """draw the Settlements table in the Settlements & Buildings tab"""
    kingdom = state.kingdom
    settlements_tab = state.tabs["settlements"]
    settlements_frame = tk.Frame(settlements_tab,borderwidth=1,relief="groove")
    settlements_frame.grid(row=2,column=0,sticky="n")
    settlement_buildings_frame = tk.Frame(settlements_tab,borderwidth=1,relief="groove")
    settlement_buildings_frame.grid(row=2,column=2,sticky="n")
    state.add_table_frame("settlements frame",settlements_frame)
    state.add_table_frame("settlement buildings frame",settlement_buildings_frame)
    ####################
    header = tk.Label(settlements_frame,text="Settlements",font=("Segoe UI",10,"bold"))
    header.grid(row=0,column=0,columnspan=50)
    hsep1 = ttk.Separator(settlements_frame,orient="horizontal")
    hsep1.grid(row=1,column=0,columnspan=50,sticky="ew")
    #################################
    def add_building(settlement,building,number):
        settlement.add_building(building)
        draw_settlements_table(state)
        settlement_buildings_table(state,settlement=settlement)
        state.write_headline_stats()
    def remove_building(settlement,building,number):
        settlement.remove_building(building)
        if building in settlement.buildings.keys():
            number.set(settlement.buildings[building])
        else:
            settlement_buildings_table(state,settlement=settlement)
        draw_settlements_table(state)
        settlement_buildings_table(state,settlement=settlement)
        state.write_headline_stats()
    def add_building_menu(state,choice,settlement):
        # choice is a stringvar that should be reset to "Choose Building"
        building = [i for i in Buildings if choice == i.name][0]
        settlement.add_building(building)
        settlement_buildings_table(state,settlement=settlement)
        draw_settlements_table(state)
        state.write_headline_stats()
    def settlement_buildings_table(state,settlement=None,parent_frame=settlement_buildings_frame):
        # draw the table showing the list of buildings in the chosen settlement
        if settlement == None:
            state.delete_frame_contents(parent_frame)
            header_frame = tk.Frame(parent_frame)
            header_frame.grid(row=0,column=0)
        else:
            state.delete_frame_contents(parent_frame)
            header_frame = tk.Frame(parent_frame)
            header = tk.Label(header_frame,text=settlement.name + " buildings",
                              font=("Segoe UI",10,"bold"),wraplength=90)
            header.grid(row=0,column=0)
            header_frame.grid(row=0,column=0)
            buildings_frame = tk.Frame(parent_frame)
            buildings_frame.grid(row=1,column=0)
            menu_var = tk.StringVar()
            menu_var.set("Add Building")
            options = [i.name for i in Buildings]
            (s,m,st) = (settlement, menu_var,state)
            building_adder = tk.OptionMenu(buildings_frame,menu_var,*options,
                                           command = lambda m=m,s=s,st=st: add_building_menu(st,m,s))
            building_adder.grid(row=0,column=0,columnspan=4)
            building_row = 1
            for building in settlement.buildings:
                number = tk.IntVar(buildings_frame,value=settlement.buildings[building])
                (s,b,n) = (settlement, building, number)
                building_name = tk.Label(buildings_frame,text=building.name)
                building_quantity = tk.Label(buildings_frame,textvariable=number)
                building_name.grid(row=building_row,column=0)
                building_quantity.grid(row=building_row,column=1,sticky="e")
                add_building_button = tk.Button(buildings_frame, text="^",
                                                command = lambda s=s,b=b,n=n: add_building(s,b,n))
                remove_building_button = tk.Button(buildings_frame, text="v",
                                                   command = lambda s=s,b=b,n=n: remove_building(s,b,n))
                add_building_button.grid(row=building_row, column=2,sticky="e")
                remove_building_button.grid(row=building_row, column=3,sticky="w")
                building_row += 1
    def draw_settlements_table(state,parent_frame=settlements_frame):
        # draw the table showing all settlements in the kingdom
        state.delete_frame_contents(parent_frame)
        header = tk.Label(settlements_frame,text="Settlements",font=("Segoe UI",10,"bold"))
        header.grid(row=0,column=0,columnspan=50)
        hsep1 = ttk.Separator(settlements_frame,orient="horizontal")
        hsep1.grid(row=1,column=0,columnspan=50,sticky="ew")
        settlement_row = 2
        for settlement in kingdom.settlements:
            name = tk.Label(parent_frame,text=settlement.name,font=("Segoe UI",10,"bold"),wraplength=90)
            name.grid(row=settlement_row,column=0,rowspan=2,padx=3)
            ############################
            level_label = tk.Label(parent_frame,text="Level: " + str(settlement.get_level()))
            type_value = tk.Label(parent_frame,text="Type: " + settlement_type(state,ob=settlement.occupied_blocks))
            level_label.grid(row=settlement_row,column=1)
            type_value.grid(row=settlement_row+1,column=1)
            capital = tk.Label(parent_frame, text = "Capital? " + str(settlement == kingdom.capital))
            capital.grid(row=settlement_row+2,column=1)
            overcrowded = tk.Label(parent_frame,text="Overcrowded? " + str(settlement.is_overcrowded()))
            overcrowded.grid(row=settlement_row+3,column=1)
            view_buildings = tk.Button(parent_frame,text="View Buildings",
                                       command = lambda s=settlement,st=state: settlement_buildings_table(st,s))
            view_buildings.grid(row=settlement_row+2,column=0)
            settlement_row += 4
            hsep2 = ttk.Separator(parent_frame,orient="horizontal")
            hsep2.grid(row=settlement_row,column=0,columnspan=50,sticky="ew")
            settlement_row += 1
    ##################################
    draw_settlements_table(state)
    settlement_buildings_table(state)




def building_search_table(state):
    """"create the building search tool in the Buildings & Settlements tab"""
    kingdom = state.kingdom
    settlements_tab = state.tabs["settlements"]
    buildings_search_frame = tk.Frame(settlements_tab,borderwidth=1,relief="groove")
    buildings_search_frame.grid(row=2,column=4,sticky="n",padx=20)
    state.add_table_frame("buildings search",buildings_search_frame)
    ########### Frame Layout ##############
    header_frame = tk.Frame(buildings_search_frame)
    header_frame.grid(row=0,column=0)
    search_frame = tk.Frame(buildings_search_frame)
    search_frame.grid(row=1,column=0)
    buildings_frame = tk.Frame(buildings_search_frame,height=600)
    buildings_frame.grid(row=2,column=0)
    ############# Header Frame Content #######
    header = tk.Label(header_frame,text="Buildings Search",font=("Segoe UI",10,"bold"))
    header.grid(row=0,column=0,sticky="nsew")
    hsep0 = ttk.Separator(header_frame,orient="horizontal")
    hsep0.grid(row=1,column=0,sticky="ew")
    #################################
    #### Search Frame Content #######
    #################################
    max_roll = tk.IntVar(search_frame,value=100)
    ekun_var = tk.IntVar(search_frame,value=0)
    residential_var = tk.IntVar(search_frame,value=0)
    unrest_var = tk.IntVar(search_frame,value=0)
    ruins_var = tk.IntVar(search_frame,value=0)
    consumption_var = tk.IntVar(search_frame,value=0)
    proficiency_var= tk.IntVar(search_frame,value=0)
    level_var = tk.IntVar(search_frame,value=0)
    ##########################
    def refresher():
        """generate a list of buildings satisfying the criteria specified using the checkboxes and dice roll field"""
        buildings_list = building_picker(max_roll=max_roll.get(), require_unrest=unrest_var.get(),
                                         require_consumption=consumption_var.get(),
                                         require_residential=residential_var.get(),
                                         require_ruins=ruins_var.get(), Ekun_modifier=ekun_var.get(),
                                         require_proficiency=proficiency_var.get(), require_level=level_var.get())
        draw_buildings_list(buildings_list)
    #####################
    ekun_checkbox = tk.Checkbutton(search_frame,text="Apply Ekundayo's DC modifier",
                                   variable=ekun_var,onvalue=1,offvalue=0,command=lambda:refresher())
    ekun_checkbox.grid(row=0,column=0)
    prof_checkbox = tk.Checkbutton(search_frame,text="Check kingdom proficiency",variable=proficiency_var,
                                   onvalue=1,offvalue=0,command=lambda:refresher())
    prof_checkbox.grid(row=0,column=1)
    level_checkbox = tk.Checkbutton(search_frame,text="Check kingdom level",variable=level_var,
                                   onvalue=1,offvalue=0,command=lambda:refresher())
    level_checkbox.grid(row=0,column=2)
    residential_checkbox = tk.Checkbutton(search_frame,text="Only show residential buildings",
                                          variable=residential_var,onvalue=1,offvalue=0,
                                          command=lambda:refresher())
    residential_checkbox.grid(row=1,column=0)
    lede = tk.Label(search_frame,text="Only show buildings that affect:")
    lede.grid(row=1,column=1,sticky="w")
    unrest_checkbox = tk.Checkbutton(search_frame,text="Unrest",variable=unrest_var,onvalue=1,offvalue=0,
                                     command=lambda:refresher())
    unrest_checkbox.grid(row=1,column=2)
    consumption_checkbox = tk.Checkbutton(search_frame,text="Consumption",variable=consumption_var,onvalue=1,
                                          offvalue=0,command=lambda:refresher())
    consumption_checkbox.grid(row=1,column=3)
    ruins_checkbox = tk.Checkbutton(search_frame,text="Ruins",variable=ruins_var,onvalue=1,offvalue=0,
                                          command=lambda:refresher())
    ruins_checkbox.grid(row=1,column=4)
    roll_to_build = tk.Label(search_frame,text="Max roll needed to build:")
    roll_to_build.grid(row=0,column=3,sticky="e")
    roll_entry = tk.Entry(search_frame,textvariable=max_roll,width=3)
    roll_entry.grid(row=0,column=4,sticky="w")
    def roll_listener(event=None):
        """redraw building list when user enters a new minimum roll value and presses Return"""
        refresher()
    roll_entry.bind("<Return>",roll_listener)
    ###############################
    ### Buildings Frame Content ###
    ###############################    
    hsep1=ttk.Separator(buildings_frame,orient="horizontal")
    hsep1.grid(row=0,column=0,sticky="ew")
    buildings_canvas = tk.Canvas(buildings_frame,width=850,height=500)  
    buildings_canvas.grid(row=1,column=0)   
    ###############
    def building_picker(max_roll=10,require_unrest=False,require_consumption=False,require_proficiency=False,
                        require_residential=False,require_ruins=False,Ekun_modifier=False,require_level=False):
        """generates a list of buildings satisfying the criteria specified in search_frame"""
        outlist = []
        for building in Buildings:
            Ekun_modifier = 2 * Ekun_modifier * (building.lumber != 0)
            if building.skill == []:
                proficiency_check = True
                roll_check = False
            else:                
                best_modifier = 0
                best_proficiency = 0
                for skill in building.skill:
                    modifier = kingdom.get_skill_modifier(skill.lower())
                    proficiency = kingdom.skills[skill.lower()]
                    if ((not require_proficiency) or proficiency >= building.proficiency) and modifier > best_modifier:
                        skill_string = skill.lower()
                        best_modifier = modifier
                        best_proficiency = proficiency
                dc_check = (max_roll + best_modifier) >= (building.DC - Ekun_modifier)
                proficiency_check = (not require_proficiency) or best_proficiency >= building.proficiency
                roll_check = dc_check and proficiency_check                        
            unrest_check = (not require_unrest) or (building.unrest != 0)
            consumption_check = (not require_consumption) or building.consumption
            residential_check = (not require_residential) or building.residential
            ruin = building.ruin + building.corruption + building.crime + building.decay + building.strife
            ruin_check = (not require_ruins) or (ruin != 0)
            level_check = (not require_level) or kingdom.level >= building.level
            if roll_check and unrest_check and consumption_check and residential_check and ruin_check and level_check:
                outlist.append(building)
        return outlist
    #########################
    def draw_buildings_list(input_list):
        """draws or refreshes the scrollable building list"""
        buildings_row = 3
        buildings_canvas.delete("all")
        inner_frame = tk.Frame(buildings_canvas)
        buildings_canvas.create_window((0,0), window=inner_frame, anchor="nw")
        for building in input_list:
            if building.skill == []: skill_string = "None"           
            else:
                skill_string = ""
                for skill in building.skill:
                    if skill != building.skill[-1]:
                        skill_string += skill + " or\n"
                    else:
                        skill_string += skill
            name = tk.Label(inner_frame,text=building.name,font=("Segoe UI",10,"bold"))
            name.grid(row=buildings_row,column=0)
            level = tk.Label(inner_frame,text="Level: " + str(building.level))
            level.grid(row=buildings_row, column=1)
            construction = tk.Label(inner_frame,text="Construction:")
            construction.grid(row=buildings_row,column=2,sticky="e")
            skill_names = tk.Label(inner_frame,text = skill_string)
            skill_names.grid(row=buildings_row,column=3,sticky="w")
            prof_and_dc = tk.Label(inner_frame,text = "DC: "+str(building.DC)+" ("+prof_dict[building.proficiency]+")")
            prof_and_dc.grid(row=buildings_row,column=4)
            lots = tk.Label(inner_frame,text="Lots: " + str(building.lots))
            lots.grid(row=buildings_row,column=5)
            cost = tk.Label(inner_frame,text="Cost: " + str(building.RP) + " RP, " +
                            str(building.lumber) + " Lumber, " + str(building.stone) + " Stone, " +
                            str(building.ore) + " Ore, " + str(building.luxuries) + " Luxuries")
            cost.grid(row=buildings_row,column=6)
            if building.ruins_text != "":
                buildings_row += 1
                ruins_label = tk.Label(inner_frame,text = "Ruins:")
                ruins_label.grid(row=buildings_row,column=0)
                ruins_text = tk.Label(inner_frame,text = building.ruins_text)
                ruins_text.grid(row=buildings_row,column=1,sticky="w")            
            item_label = tk.Label(inner_frame, text="Item Bonuses:")
            item_label.grid(row=buildings_row+1,column=0)
            item_text = tk.Label(inner_frame,text = building.item_bonus_text,wraplength=700,justify="left")
            item_text.grid(row=buildings_row+1,column=1,columnspan=50,sticky="w")
            desc_label = tk.Label(inner_frame,text="Effects:")
            desc_label.grid(row = buildings_row+2,column=0,sticky="n")
            description = tk.Label(inner_frame,text=building.effects,wraplength=700,justify="left")
            description.grid(row=buildings_row+2,column=1,columnspan=50,sticky="w")
            buildings_row += 3
            hsep3=ttk.Separator(inner_frame,orient="horizontal")
            hsep3.grid(row=buildings_row,column=0,columnspan=50,sticky="ew")
            buildings_row += 1        
    draw_buildings_list(building_picker(max_roll=100))
    vscroll = tk.Scrollbar(buildings_frame,orient="vertical",command=buildings_canvas.yview)
    vscroll.grid(row=0,column=1,rowspan=2000,sticky="ns")
    buildings_canvas.configure(yscrollcommand=vscroll.set(0,0))
    buildings_canvas.bind("<Configure>",
                          lambda e: buildings_canvas.configure(scrollregion = buildings_canvas.bbox("all")))    
