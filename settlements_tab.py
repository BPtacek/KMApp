# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:46:48 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
from buildings import *
from constants import *

def settlement_type(state,ob):
    # Int -> String. Take settlement's level and number of occupied blocks, return its text classification        
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
    # draw the Settlements table in the Settlements & Buildings tab
    kingdom = state.kingdom
    settlements_tab = state.tabs[2]
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
        # create the building search tool in the Buildings & Settlements tab
        if settlement == None:
            state.delete_frame_contents(parent_frame)
            header_frame = tk.Frame(parent_frame)
            header_frame.grid(row=0,column=0)        
        else:
            state.delete_frame_contents(parent_frame)
            header_frame = tk.Frame(parent_frame)
            header = tk.Label(header_frame,text=settlement.name + " buildings",font=("Segoe UI",10,"bold"))
            header.grid(row=0,column=0)
            header_frame.grid(row=0,column=0)        
            buildings_frame = tk.Frame(parent_frame)
            buildings_frame.grid(row=1,column=0)
            add_building_label = tk.Label(buildings_frame, text = "Add Building:")
            add_building_label.grid(row=0,column=0)
            menu_var = tk.StringVar()
            menu_var.set("Choose Building")
            options = [i.name for i in Buildings]
            (s,m,st) = (settlement, menu_var,state)
            building_adder = tk.OptionMenu(buildings_frame,menu_var,*options,
                                           command = lambda m=m,s=s,st=st: add_building_menu(st,m,s))
            building_adder.grid(row=0,column=1,columnspan=3)
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
        state.delete_frame_contents(parent_frame)
        header = tk.Label(settlements_frame,text="Settlements",font=("Segoe UI",10,"bold"))
        header.grid(row=0,column=0,columnspan=50)
        hsep1 = ttk.Separator(settlements_frame,orient="horizontal")
        hsep1.grid(row=1,column=0,columnspan=50,sticky="ew") 
        settlement_row = 2
        for settlement in kingdom.settlements:
            name = tk.Label(parent_frame,text=settlement.name,font=("Segoe UI",10,"bold"))
            name.grid(row=settlement_row,column=0,rowspan=2,padx=3)
            ############################                
            level_label = tk.Label(parent_frame,text="Level: " + str(settlement.get_level()))                
            type_value = tk.Label(parent_frame,text="Type: " + settlement_type(state,ob=settlement.occupied_blocks))            
            level_label.grid(row=settlement_row,column=1)
            type_value.grid(row=settlement_row,column=2,padx=2)
            num_residences = tk.Label(parent_frame,text= "Residences: " + 
                                      str(sum([j for (i,j) in settlement.buildings.items() if i.residential])))
            num_residences.grid(row=settlement_row+2,column=1,padx=2)
            capital = tk.Label(parent_frame, text = "Capital? " + str(settlement == kingdom.capital))
            capital.grid(row=settlement_row+1,column=1)
            overcrowded = tk.Label(parent_frame,text="Overcrowded? " + str(settlement.is_overcrowded()))
            overcrowded.grid(row=settlement_row+1,column=2)
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
    # create the building search tool in the Buildings & Settlements tab
    kingdom = state.kingdom
    settlements_tab = state.tabs[2]
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
        # generate a list of buildings satisfying the criteria specified using the checkboxes and dice roll field            
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
        # redraw building list when user enters a new minimum roll value and presses Return
        refresher()
    roll_entry.bind("<Return>",roll_listener)
    ###############################
    ### Buildings Frame Content ###
    ###############################
    buildings_header = tk.Frame(buildings_frame,width=850)
    buildings_header.grid(row=0,column=0)
    buildings_canvas = tk.Canvas(buildings_frame,width=850,height=500)        
    buildings_canvas.grid(row=1,column=0)     
    vscroll = tk.Scrollbar(buildings_frame,orient="vertical",command=buildings_canvas.yview)
    vscroll.grid(row=1,column=1,rowspan=500,sticky="ns")
    buildings_canvas.configure(yscrollcommand=vscroll.set)
    buildings_canvas.bind("<Configure>", 
                          lambda e: buildings_canvas.configure(scrollregion = buildings_canvas.bbox("all")))        
    # parameters to force alignment of the columns in the search header frame and scrollable buildings list
    name_width = 17
    skill_width = 10
    prof_width = 10
    dc_width = 5
    level_width = 5
    lots_width = 5 
    rp_width = 7
    materials_width = 10
    description_width = 48        
    ## generate the search header frame's content
    hsep1=ttk.Separator(buildings_header,orient="horizontal")
    hsep1.grid(row=0,column=0,columnspan=50,sticky="ew")   
    building_name = tk.Label(buildings_header,text="Name",width=name_width)
    building_name.grid(row=1,column=0,sticky="ew")
    building_skill = tk.Label(buildings_header,text="Skill",width=skill_width)
    building_skill.grid(row=1,column=1,sticky="ew")
    proficiency = tk.Label(buildings_header,text="Proficiency",width=prof_width)
    proficiency.grid(row=1,column=2,sticky="ew")
    building_DC = tk.Label(buildings_header,text="DC",width=dc_width)
    building_DC.grid(row=1,column=3,sticky="ew")
    level = tk.Label(buildings_header,text="Level",width=level_width)
    level.grid(row=1,column=4,sticky="ew")
    lots_label = tk.Label(buildings_header,text="Lots",width=lots_width)
    lots_label.grid(row=1,column=5,sticky="ew")
    RP_label = tk.Label(buildings_header,text="RP Cost",width=rp_width)
    RP_label.grid(row=1,column=6,sticky="ew")
    materials_label = tk.Label(buildings_header,text="Material \n Cost",width=materials_width)
    materials_label.grid(row=1,column=7,sticky="ew")
    description = tk.Label(buildings_header,text="Description",width=description_width)
    description.grid(row=1,column=8,columnspan=3,sticky="ew")
    hsep2=ttk.Separator(buildings_header,orient="horizontal")
    hsep2.grid(row=2,column=0,columnspan=50,sticky="ew")        
    ###############                
    def building_picker(max_roll=10,require_unrest=False,require_consumption=False,require_proficiency=False,
                        require_residential=False,require_ruins=False,Ekun_modifier=False,require_level=False):
        # generates a list of buildings satisfying the criteria specified in search_frame
        outlist = []  
        for building in Buildings:
            Ekun_modifier = 2 * Ekun_modifier * (building.lumber != 0)
            if building.skill.lower() in Kingdom_skills:
                modifier = kingdom.get_modifier(building.skill.lower())
                proficiency = kingdom.skills[building.skill.lower()]
                dc_check = (max_roll + modifier) >= (building.DC - Ekun_modifier) 
                proficiency_check = (not require_proficiency) or proficiency >= building.proficiency
                roll_check = dc_check and proficiency_check
            else: roll_check, proficiency_check = False, True
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
        # draws or refreshes the scrollable building list
        buildings_row = 3            
        buildings_canvas.delete("all") 
        inner_frame = tk.Frame(buildings_canvas)
        buildings_canvas.create_window((0,0), window=inner_frame, anchor="nw")
        for building in input_list:
            name = tk.Label(inner_frame,text=building.name,width=name_width)
            name.grid(row=buildings_row,column=0)
            skill = tk.Label(inner_frame,text=building.skill,width=skill_width)
            skill.grid(row=buildings_row, column=1)
            prof = tk.Label(inner_frame,text=prof_dict[building.proficiency],width=prof_width)
            prof.grid(row=buildings_row,column=2)
            dc = tk.Label(inner_frame,text=building.DC,width=dc_width)
            dc.grid(row=buildings_row,column=3)
            level = tk.Label(inner_frame,text=building.level,width=level_width)
            level.grid(row=buildings_row, column=4)
            lots = tk.Label(inner_frame,text=building.lots,width=lots_width)
            lots.grid(row=buildings_row,column=5)
            rp = tk.Label(inner_frame,text=building.RP,width=rp_width)
            rp.grid(row=buildings_row,column=6)
            materials = tk.Frame(inner_frame,width=materials_width)
            materials.grid(row=buildings_row,column=7)
            lumber = tk.Label(materials,text="Lumber: " + str(building.lumber))
            lumber.grid(row=0,column=0)
            stone = tk.Label(materials,text="Stone: " + str(building.stone))
            stone.grid(row=1,column=0)
            ore = tk.Label(materials,text="Ore: " + str(building.ore))
            ore.grid(row=2,column=0)
            luxuries = tk.Label(materials,text="Luxuries: " + str(building.luxuries))
            luxuries.grid(row=3,column=0)
            description = tk.Label(inner_frame,text="Lorem ipsum dolor...",width=description_width)
            description.grid(row=buildings_row,column=8,columnspan=3)
            buildings_row += 1
            hsep3=ttk.Separator(inner_frame,orient="horizontal")
            hsep3.grid(row=buildings_row,column=0,columnspan=50,sticky="ew")
            buildings_row += 1
    draw_buildings_list(building_picker(max_roll=100))