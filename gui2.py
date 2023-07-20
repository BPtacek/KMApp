# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:41:37 2023

@author: dtbla
"""
import json
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from math import cos, sin, sqrt, radians

from buildings import *

image1 = Image.open("GridlessMap75.jpeg")

def main(kingdom=Greenbelt):
    w1 = tk.Tk()
    w1.title("Kingdom Management!")

    def donothing():
        print("I am doing nothing!")
    
    menubar = tk.Menu(w1)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=donothing)
    filemenu.add_command(label="Open", command=donothing)
    filemenu.add_command(label="Save", command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=donothing)
    menubar.add_cascade(label="File", menu=filemenu)
    w1.config(menu=menubar) 
    
    header = tk.Label(w1, text=kingdom.name)
    header.grid(row=0,column=0,columnspan=5000)
    
    tabControl = ttk.Notebook(w1)
    kingdom_overview = ttk.Frame(tabControl)
    kingdom_details = ttk.Frame(tabControl)
    settlements_tab = ttk.Frame(tabControl)    
    tabControl.add(kingdom_overview, text="Kingdom Overview")
    tabControl.add(kingdom_details, text="Kingdom Details")
    tabControl.add(settlements_tab, text="Settlements & Buildings")       
    tabControl.grid(row=1, column=0, columnspan=5000)    
    tabs = [kingdom_overview,kingdom_details,settlements_tab]
    
    attributes = ["loyalty","stability","culture","economy"]
    attribute_variables = {i:tk.IntVar(w1,value=kingdom.get_attribute(i)) for i in attributes}
    skill_modifiers = {i:tk.IntVar(w1,value=kingdom.get_modifier(i)) for i in Kingdom_skills.keys()}
    prof_dict = {0:"Untrained",1:"Trained",2:"Expert",3:"Master",4:"Legendary"}
    proficiency_variables = {i:tk.StringVar(w1) for i in Kingdom_skills.keys()}
    ruin_variables = {i:tk.StringVar(w1,value=kingdom.ruins[i]) for i in Ruins}      
      
    def write_headline_stats():        
        for tab in tabs:
            headline_frame = tk.Frame(tab)
            headline_frame.grid(column=0, row=1, columnspan=5000,sticky="w")
            top_separator = ttk.Separator(headline_frame, orient="horizontal")
            top_separator.grid(column=0, row=0, columnspan=5000, sticky="ew")
            bottom_separator = ttk.Separator(headline_frame, orient="horizontal")
            bottom_separator.grid(column=0, row=2, columnspan=5000, sticky="ew")       
            #############            
            level_label = tk.Label(headline_frame, text="Level: " + str(kingdom.level))            
            level_label.grid(row=1, column=0,padx=10)
            ################            
            control_label = tk.Label(headline_frame, text="Control DC: " + str(kingdom.control_DC))
            control_label.grid(row=1, column=1,padx=10)
            #########################            
            hexes_label = tk.Label(headline_frame, text="Claimed Hexes: " + str(len(kingdom.claimed_hexes))) 
            hexes_label.grid(row=1, column=2,padx=10)
            ########################
            unrest_label = tk.Label(headline_frame, text="Unrest: " + str(kingdom.unrest))
            unrest_label.grid(row=1, column=3, padx=10)
            ############################
            food_label = tk.Label(headline_frame, text="Food: " + str(kingdom.resources["food"][0]))
            food_label.grid(row=1, column=4, padx=10)
            food_capacity_label = tk.Label(headline_frame, text="Food Consumed/Turn: " + str(kingdom.get_consumption()))
            food_capacity_label.grid(row=1, column=5, padx=10)
            food_turn_label = tk.Label(headline_frame, text="Food Gained/Turn: " + str(kingdom.resources["food"][2]))
            food_turn_label.grid(row=1, column=6, padx=10)
            ##############################
            resource_dice_label = tk.Label(headline_frame, text = "Base Resource Dice: " + kingdom.get_base_resource_die_string())
            resource_dice_label.grid(row=1, column=8, padx=10)
            ##################################
            ruin_startcol=9
            for ruin in Ruins:
                ruin_label = tk.Label(headline_frame,text = ruin.title() + ": " + str(kingdom.ruins[ruin]))
                ruin_label.grid(row=1, column=ruin_startcol,padx=10)
                ruin_startcol += 1
            
    write_headline_stats()
    # the above displays the headline kingdom stats - level, control DC, number claimed hexes, unrest, food status, ruins
    
    # the above draws the cells of the skills/attributes table
    hexagon_side_length = 30
    hex_angle = 60
    map_canvas = tk.Canvas(kingdom_overview, width=1530, height=540)
    worldmap = ImageTk.PhotoImage(image1)
    map_canvas.create_image(0, 0, anchor="nw", image=worldmap)

    # the above defines key hex grid parameters, creates the world map window, and places it beside the attribute table
    def draw_hexagon(x=0, y=0, color="black", linewidth=0):
        # draws a single hexagon
        start_x = x
        start_y = y
        length = hexagon_side_length
        angle = hex_angle
        for i in range(6):
            end_x = start_x + length * cos(radians(30 + angle * i))
            end_y = start_y + length * sin(radians(30 + angle * i))
            map_canvas.create_line(start_x,
                                   start_y,
                                   end_x,
                                   end_y,
                                   fill=color,
                                   width=linewidth)
            start_x = end_x
            start_y = end_y

    grid_vertical_offset = -1.4 * hexagon_side_length  # parameter to adjust grid position so it matches in-game map
    hex_center_list = []

    def draw_hex_grid():
        # draws a grid of hexagons over the world map. hexagons are drawn starting from the "top" vertex.     
        length = hexagon_side_length  # renaming for brevity
        for c in range(30):
            for r in range(13):
                if r % 2 != 0:
                    x_offset = 0.5 * length * sqrt(3)
                else:
                    x_offset = 0
                draw_hexagon(x_offset + c * length * sqrt(3), r * length * 1.5 + grid_vertical_offset)
                h = (x_offset + c * length * sqrt(3), length + r * length * 1.5 + grid_vertical_offset)
                hex_center_list.append(h)

    draw_hex_grid()

    def identify_hex(mouse_x, mouse_y):
        # returns the pixel coordinates of the top vertex of the grid hex where the mouse was clicked
        nearest_hex_center = (0, 0)
        nearest_hex_distance = 5000
        for (hex_x, hex_y) in hex_center_list:
            distance = sqrt((mouse_x - hex_x) ** 2 + (mouse_y - hex_y) ** 2)
            if distance < nearest_hex_distance:
                nearest_hex_center = (hex_x, hex_y)
                nearest_hex_distance = distance
        return (nearest_hex_center[0], nearest_hex_center[1] - hexagon_side_length)
    
    def right_click_add_hex(event=None):
        # add a hex to kingdom.claimed_hexes on right click and draw a red border around the newly claimed hex
        adjusted_hex_coordinate = identify_hex(event.x, event.y)
        kingdom.add_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
        draw_kingdom_borders()
        write_headline_stats()

    def middle_click_remove_hex(event=None):
        # remove a claimed hex on middle-click and redraw the world map to remove red border around the lost hex
        adjusted_hex_coordinate = identify_hex(event.x, event.y)
        kingdom.remove_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
        map_canvas.delete("all")  # horrible hacky strategy: update map by deleting it and redrawing everything
        map_canvas.create_image(0, 0, anchor="nw", image=worldmap)
        draw_hex_grid()
        draw_kingdom_borders()
        write_headline_stats()

    map_canvas.bind("<Button-3>", right_click_add_hex)
    map_canvas.bind("<Button-2>", middle_click_remove_hex)

    def draw_kingdom_borders():
        # draw a thick red line over the hex grid around the kingdom's external borders
        map_canvas.delete("all")
        map_canvas.create_image(0, 0, anchor="nw", image=worldmap)
        draw_hex_grid()
        linepoints1 = []
        def truncate(a): # a is a float; discard everything after first 5 decimal places
            return float(f'{a:.5f}')
        for (x, y) in kingdom.claimed_hexes:
            start_x = x
            start_y = y
            length = hexagon_side_length
            angle = hex_angle
            for i in range(6):
                end_x = start_x + length * cos(radians(30 + angle * i))
                end_y = start_y + length * sin(radians(30 + angle * i))
                x1 = truncate(start_x)
                x2 = truncate(end_x)
                y1 = truncate(start_y)
                y2 = truncate(end_y)                
                linepoints1.append(((x1,y1),(x2,y2)))
                start_x = end_x
                start_y = end_y       
        linepoints2 = []
        for ((x1,y1),(x2,y2)) in linepoints1:
            if ((x2,y2),(x1,y1)) not in linepoints1:
                linepoints2.append(((x1,y1),(x2,y2)))                    
        for ((x1,y1),(x2,y2)) in linepoints2:
                map_canvas.create_line(x1,y1,x2,y2,fill="red",width=3)                
    draw_kingdom_borders()
    map_canvas.grid(row=4, column=0, rowspan=30, columnspan=300)

    # the above adds the world map image, draws the hex grid, and controls addition/removal of kingdom hexes

    def update_skill_modifiers():
        for skill in Kingdom_skills.keys():
            skill_modifiers[skill].set(kingdom.get_modifier(skill))
        
    def update_attributes():
        for attribute in attributes:
            attribute_variables[attribute].set(kingdom.get_attribute(attribute))
        update_skill_modifiers()
        
    def increase_skill(skill):
        kingdom.increase_skill(skill)
        skill_modifiers[skill].set(kingdom.get_modifier(skill))
        update_proficiencies()
    
    def reduce_skill(skill):
        kingdom.reduce_skill(skill)
        skill_modifiers[skill].set(kingdom.get_modifier(skill))
        update_proficiencies()
        
    def increase_attribute(attribute):
        kingdom.increase_attribute(attribute)
        update_attributes()
    
    def reduce_attribute(attribute):
        kingdom.reduce_attribute(attribute)
        update_attributes()    
    
    def update_proficiencies():        
        for skill in Kingdom_skills.keys():
            prof = kingdom.skills[skill]
            str = prof_dict[prof]
            proficiency_variables[skill].set(str)    
    
    def draw_attribute_overview():
        attribute_table_startrow=38
        attribute_table_startcol = 0
        for attribute in attributes:
            attribute_frame = tk.Frame(kingdom_overview,borderwidth=1,relief="groove")
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
    
    draw_attribute_overview()
                
    def export_kingdom_as_file(file_name, kingdom=Greenbelt, print_only=False):
        file_name = file_name if file_name.endswith(".json") else file_name + ".json"
        kingdom_data = kingdom.export_kingdom_data()
        if print_only:
            print(json.dumps(kingdom_data, indent=4))
            return
        with open(f"{file_name}", "w") as f:
            json.dump(kingdom_data, f, indent=4)   
     
    
    def draw_attribute_details():
        # draw the detailed attributes/skills/leaders table in the Kingdom Details tab
        attribute_table_frame = tk.Frame(kingdom_details,borderwidth=1,relief="groove")
        attribute_table_header = tk.Label(attribute_table_frame,
                                          text="Kingdom Attributes, Skills, & Leaders",font=("Segoe UI",10,"bold"))
        attribute_table_header.grid(row=0,column=0)
        attribute_table_frame.grid(row=5, column=0, rowspan=100,padx=10)   
        attribute_table_startrow=6
        attribute_table_startcol = 0
        update_proficiencies()
        for attribute in attributes:
            attribute_frame = tk.Frame(attribute_table_frame,borderwidth=1,relief="groove")
            attribute_header = tk.Frame(attribute_frame)
            attribute_frame.grid(row = attribute_table_startrow, column = attribute_table_startcol, sticky="nsew")
            attribute_header.grid(row=0,column=0,columnspan=8)
            header_label = tk.Label(attribute_header, text = attribute.title() + ": ")
            header_value = tk.Label(attribute_header, textvariable=attribute_variables[attribute])
            attribute_up_button = tk.Button(attribute_header, text="^",
                                            command = lambda a=attribute: increase_attribute(a))
            attribute_down_button = tk.Button(attribute_header, text="v",
                                            command = lambda a=attribute: reduce_attribute(a))            
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
                                                command = lambda s=skill: increase_skill(s))
                    skill_down_button = tk.Button(attribute_frame, text="v",
                                                command = lambda s=skill: reduce_skill(s))   
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

    draw_attribute_details()
        
    def draw_level_table():
        # draw the level/XP/XP gain table in the Kingdom Details tab
        level_table_frame = tk.Frame(kingdom_details, borderwidth=1,relief="groove")
        level_table_frame.grid(row=5, column=2,padx=10,sticky="n")
        header_frame = tk.Frame(level_table_frame)
        header_frame.grid(row=0, column = 0, columnspan=50)
        header = tk.Label(header_frame,text="Kingdom Level and XP",font=("Segoe UI",10,"bold"))
        header.grid(row=0, column=0, columnspan=50,padx=5)
        level_frame = tk.Frame(level_table_frame)
        level_frame.grid(row=1, column = 0, columnspan=50,sticky="w",padx=5)
        level_label = tk.Label(level_frame, text = "Kingdom Level: " + str(kingdom.level))
        level_label.grid(row=0, column=0,sticky="w")
        def increase_level():
            kingdom.increase_level()
            update_skill_modifiers()
            write_headline_stats()
            draw_level_table()
        def reduce_level():
            kingdom.reduce_level()
            update_skill_modifiers()
            write_headline_stats()
            draw_level_table()
        level_up_button = tk.Button(level_frame, text="^",
                                    command = lambda: increase_level())
        level_down_button = tk.Button(level_frame, text="v",
                                      command = lambda: reduce_level())
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
            update_skill_modifiers()
            write_headline_stats()
            draw_level_table()
        xp_entry.bind("<Return>",xp_listener)
        xp_label.grid(row=0, column=0,padx=5)        
        increase_xp.grid(row=0, column=1)
        xp_entry.grid(row=0, column=2)
        xp_frame.grid(row=2,column=0)        
    
    draw_level_table()
    
    def draw_resource_table():
        # draw the resources table in the Kingdom Details tab
        resource_table_frame = tk.Frame(kingdom_details, borderwidth=1,relief="groove")
        resource_table_frame.grid(row=6, column=2,sticky="n")
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
    
    draw_resource_table()
    
    def draw_unrest_table():
        # draw the unrest table in the Kingdom Details tab
        unrest_frame = tk.Frame(kingdom_details,borderwidth=1,relief="groove")
        unrest_frame.grid(row=7,column=2,sticky="n")
        header_frame = tk.Frame(unrest_frame)
        header_frame.grid(row=0, column = 0, columnspan=50)
        header = tk.Label(header_frame,text="Unrest",font=("Segoe UI",10,"bold"))
        header.grid(row=0, column=0, columnspan=50,padx=5)
        main_frame = tk.Frame(unrest_frame)
        main_frame.grid(row=1,column=0)
        unrest_label = tk.Label(main_frame,text="Unrest: " + str(kingdom.unrest))
        def unrest_penalty():
            penalties = {0:0,1:1,5:2,10:3,15:4}
            return -1*max([penalties[i] for i in penalties.keys() if kingdom.unrest >= i])
        unrest_penalty = tk.Label(main_frame, text="Unrest Penalty: " + str(unrest_penalty()))
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
            write_headline_stats()
            draw_unrest_table()
        unrest_entry.bind("<Return>",unrest_listener)
        
    draw_unrest_table()
    
    def draw_ruins_table():
        # draw the ruins table in the Kingdom Details tab
        ruins_frame = tk.Frame(kingdom_details,borderwidth=1,relief="groove")
        ruins_frame.grid(row=8,column=2,sticky="n")
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
    
    draw_ruins_table()
    
    def draw_settlements_table():
        settlements_frame = tk.Frame(settlements_tab,borderwidth=1,relief="groove")
        settlements_frame.grid(row=2,column=0,sticky="n")
        ####################
        header_frame=tk.Frame(settlements_frame)
        header_frame.grid(row=0,column=0,columnspan=50)
        header = tk.Label(header_frame,text="Settlements",font=("Segoe UI",10,"bold"))
        header.grid(row=0,column=0,columnspan=50)
        hsep1 = ttk.Separator(settlements_frame,orient="horizontal")
        hsep1.grid(row=1,column=0,columnspan=50,sticky="ew")
        #################################
        name_label = tk.Label(settlements_frame,text="Name")
        name_label.grid(row=2,column=0)
        level_label = tk.Label(settlements_frame,text="Level",padx=2)
        level_label.grid(row=2,column=1)
        type_label = tk.Label(settlements_frame,text="Type",padx=2)
        type_label.grid(row=2,column=2)        
        residences_label = tk.Label(settlements_frame,text="Residences",padx=2)
        residences_label.grid(row=2,column=3)
        buildings_label = tk.Label(settlements_frame,text="Buildings",padx=2)
        buildings_label.grid(row=2,column=4,columnspan=6)
        hsep2 = ttk.Separator(settlements_frame,orient="horizontal")
        hsep2.grid(row=3,column=0,columnspan=50,sticky="ew")
        #####################################
        settlement_row = 4
        for settlement in kingdom.settlements:            
            def settlement_type(occupied_blocks):
                types = {1:"Village",4:"Town",9:"City",14:"Metropolis"}
                key = min([i for i in types.keys() if occupied_blocks <= i])
                return types[key]            
            name = tk.Label(settlements_frame,text=settlement.name)
            level = tk.Label(settlements_frame,text=settlement.level)
            type_value = tk.Label(settlements_frame,text=settlement_type(settlement.occupied_blocks))
            name.grid(row=settlement_row,column=0)
            level.grid(row=settlement_row,column=1)
            type_value.grid(row=settlement_row,column=2)
            num_residences = tk.Label(settlements_frame,
                                      text=str(sum([j for (i,j) in settlement.buildings.items() if i.residential])))
            num_residences.grid(row=settlement_row,column=3)
            buildings_frame = tk.Frame(settlements_frame)
            buildings_frame.grid(row=settlement_row,column=4)
            building_row = 0
            for building in settlement.buildings:
                building_name = tk.Label(buildings_frame,text=building.name)
                building_quantity = tk.Label(buildings_frame,text=str(settlement.buildings[building]))
                building_name.grid(row=building_row,column=0)
                building_quantity.grid(row=building_row,column=1)
                building_row += 1            
            settlement_row += 1
            hsep2 = ttk.Separator(settlements_frame,orient="horizontal")
            hsep2.grid(row=settlement_row,column=0,columnspan=50,sticky="ew")
            settlement_row += 1          
                
    draw_settlements_table()
    
    def building_finder():
        master_frame = tk.Frame(settlements_tab)
        master_frame.grid(row=2,column=2,sticky="n",padx=20)        
        #########################
        header_frame = tk.Frame(master_frame)        
        header = tk.Label(header_frame,text="Buildings Search",font=("Segoe UI",10,"bold"))
        header.grid(row=0,column=0,columnspan=500,sticky="nsew")
        hsep0 = ttk.Separator(header_frame,orient="horizontal")
        hsep0.grid(row=1,column=0,columnspan=500,sticky="ew")        
        header_frame.grid(row=0,column=0,columnspan=500)
        ####################
        search_frame = tk.Frame(master_frame)
        search_frame.grid(row=1,column=0)
        feasible_to_build = tk.Label(search_frame,text="Buildable on a 10 or lower?")
        feasible_to_build.grid(row=0,column=0)
        ####################
        buildings_frame = tk.Frame(master_frame,height=800)
        buildings_frame.grid(row=2,column=0)
        buildings_header = tk.Frame(buildings_frame,width=850)
        buildings_header.grid(row=0,column=0)
        buildings_canvas = tk.Canvas(buildings_frame,width=850,height=500)        
        buildings_canvas.grid(row=1,column=0)     
        vscroll = tk.Scrollbar(buildings_frame,orient="vertical",command=buildings_canvas.yview)
        vscroll.grid(row=1,column=1,rowspan=500,sticky="ns")
        buildings_canvas.configure(yscrollcommand=vscroll.set)
        buildings_canvas.bind("<Configure>", 
                              lambda e: buildings_canvas.configure(scrollregion = buildings_canvas.bbox("all")))
        inner_frame = tk.Frame(buildings_canvas)
        buildings_canvas.create_window((0,0), window=inner_frame, anchor="nw")
        #############################
        name_width = 17
        skill_width = 10
        dc_width = 5
        lots_width = 5 
        rp_width = 7
        materials_width = 10
        residential_width = 8 
        unrest_width = 8 
        ruins_width = 10
        consumption_width = 14
        description_width = 20
        ###########################
        hsep1=ttk.Separator(buildings_header,orient="horizontal")
        hsep1.grid(row=0,column=0,columnspan=50,sticky="ew")   
        building_name = tk.Label(buildings_header,text="Name",width=name_width)
        building_name.grid(row=1,column=0,sticky="ew")
        building_skill = tk.Label(buildings_header,text="Skill",width=skill_width)
        building_skill.grid(row=1,column=1,sticky="ew")
        building_DC = tk.Label(buildings_header,text="DC",width=dc_width)
        building_DC.grid(row=1,column=2,sticky="ew")
        lots_label = tk.Label(buildings_header,text="Lots",width=lots_width)
        lots_label.grid(row=1,column=3,sticky="ew")
        RP_label = tk.Label(buildings_header,text="RP Cost",width=rp_width)
        RP_label.grid(row=1,column=4,sticky="ew")
        materials_label = tk.Label(buildings_header,text="Material \n Cost",width=materials_width)
        materials_label.grid(row=1,column=5,sticky="ew")
        residence_label = tk.Label(buildings_header,text="Residential?",width=residential_width)
        residence_label.grid(row=1,column=6,sticky="ew")
        affects_unrest = tk.Label(buildings_header,text="Affects \n Unrest?",width=unrest_width)
        affects_unrest.grid(row=1,column=7,sticky="ew")
        affects_ruins = tk.Label(buildings_header,text="Affects \n Ruins?",width=ruins_width)
        affects_ruins.grid(row=1,column=8,sticky="ew")
        affects_consumption = tk.Label(buildings_header,text="Affects \n Consumption?",width=consumption_width)
        affects_consumption.grid(row=1,column=9,sticky="ew")
        description = tk.Label(buildings_header,text="Description",width=description_width)
        description.grid(row=1,column=10,sticky="ew")
        hsep2=ttk.Separator(buildings_header,orient="horizontal")
        hsep2.grid(row=2,column=0,columnspan=50,sticky="ew")        
        ###############
        buildings_row = 3
        for building in Buildings:
            name = tk.Label(inner_frame,text=building.name,width=name_width)
            name.grid(row=buildings_row,column=0)
            skill = tk.Label(inner_frame,text=building.skill,width=skill_width)
            skill.grid(row=buildings_row, column=1)
            dc = tk.Label(inner_frame,text=building.DC,width=dc_width)
            dc.grid(row=buildings_row,column=2)
            lots = tk.Label(inner_frame,text=building.lots,width=lots_width)
            lots.grid(row=buildings_row,column=3)
            rp = tk.Label(inner_frame,text=building.RP,width=rp_width)
            rp.grid(row=buildings_row,column=4)
            materials = tk.Frame(inner_frame,width=materials_width)
            materials.grid(row=buildings_row,column=5)
            lumber = tk.Label(materials,text="Lumber: " + str(building.lumber))
            lumber.grid(row=0,column=0)
            stone = tk.Label(materials,text="Stone: " + str(building.stone))
            stone.grid(row=1,column=0)
            ore = tk.Label(materials,text="Ore: " + str(building.ore))
            ore.grid(row=2,column=0)
            luxuries = tk.Label(materials,text="Luxuries: " + str(building.luxuries))
            luxuries.grid(row=3,column=0)
            residential = tk.Label(inner_frame,text=str(building.residential),width=residential_width)
            residential.grid(row=buildings_row,column=6)
            unrest = tk.Label(inner_frame,text=str(building.unrest),width=unrest_width)
            unrest.grid(row=buildings_row,column=7)
            ruins = tk.Label(inner_frame,text=str("Placeholder"),width=ruins_width)
            ruins.grid(row=buildings_row,column=8)
            consumption = tk.Label(inner_frame,text=str(building.consumption),width=consumption_width)
            consumption.grid(row=buildings_row,column=9)
            description = tk.Label(inner_frame,text="Lorem ipsum dolor...",width=description_width)
            description.grid(row=buildings_row,column=10)
            buildings_row += 1
            hsep3=ttk.Separator(inner_frame,orient="horizontal")
            hsep3.grid(row=buildings_row,column=0,columnspan=50,sticky="ew")
            buildings_row += 1        
    building_finder()
    
    w1.mainloop()