# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:41:37 2023

@author: dtbla
"""
import tkinter as tk
from tkinter.ttk import Separator
from PIL import ImageTk,Image
from math import cos, sin, sqrt, radians

from buildings import *

Noktown = Settlement("Noktown", (1013.2497224277931, 273.0),2,
                    {Houses:2,GeneralStore:1,TownHall:1,AlchemyLab:1,Mill:1,PopularTavern:1,WoodenWall:1})
Lizards = Settlement("Isle of the Lizard King",(909.3266739736605, 363.0),1,{Houses:1,Mill:1,Shrine:1})
Tatzlford = Settlement("Tatzlford",(883.3459118601273, 228.0),2,
                       {Houses:1,TownHall:1,Inn:1,Orphanage:1,Barracks:1})
Greenbelt = Kingdom("Greenbelt Republic", [],
                    5, 0, {i:0 for i in Ruins},[Noktown,Lizards,Tatzlford],
                    {"culture":14,"economy":16,"loyalty":14,"stability":14},{i:0 for i in Kingdom_skills.keys()},
                    {i:"filled" for i in Advisors.keys()},{},[30,6,13],{"food":[5,8,2]})

image1 = Image.open("GridlessMap75.jpeg")

def main(kingdom=Greenbelt):
    w1=tk.Tk()
    w1.title("Kingdom Management!")
    # Width, height in pixels
    header = tk.Label(w1,text=kingdom.name + " Kingdom Sheet")
    header.grid(row = 0, column = 0, pady = 2, padx = 2, columnspan = 5000)
    header_separator = Separator(w1, orient="horizontal")
    header_separator.grid(column = 0, row = 1, columnspan = 5000, sticky="ew")
    # the above creates the app header
    def write_kingdom_stats():
        header_frame = tk.Frame(w1)
        header_frame.grid(row=2, column=0, columnspan=80)
        level_frame = tk.Frame(header_frame)
        level_label = tk.Label(level_frame, text = "Level: " + str(kingdom.level))        
        increase_button = tk.Button(level_frame,text = "^", command = lambda:increase_level())        
        reduce_button = tk.Button(level_frame,text = "v",command = lambda:reduce_level())
        level_label.grid(row = 0, column = 0)        
        increase_button.grid(row=0, column=1)
        reduce_button.grid(row=0, column=2)
        level_frame.grid(row = 0, column = 0, padx=10)
        control_label = tk.Label(header_frame, text = "Control DC: " + str(kingdom.control_DC))
        control_label.grid(row=0, column=1, padx=10)
        hexes_label = tk.Label(header_frame, text = "Claimed Hexes: " + str(len(kingdom.claimed_hexes)))
        hexes_label.grid(row=0, column=3, padx=10)        
        unrest_label = tk.Label(header_frame,text = "Unrest: " + str(kingdom.unrest))
        unrest_label.grid(row=0, column=4, padx=10)                
        food_label = tk.Label(header_frame,text="Food: " + str(kingdom.resources["food"][0]))
        food_label.grid(row=0, column=5, padx=10)
        food_capacity_label = tk.Label(header_frame, text = "Food Storage Capacity: " + str(kingdom.resources["food"][1]))
        food_capacity_label.grid(row=0, column=6, padx=10)
        food_turn_label = tk.Label(header_frame, text = "Food Per Turn: " + str(kingdom.resources["food"][2]))
        food_turn_label.grid(row=0, column=7, padx=10)
    def increase_level():
        kingdom.increase_level()
        write_kingdom_stats()
        draw_attribute_table()
    def reduce_level():
        kingdom.reduce_level()
        write_kingdom_stats()
        draw_attribute_table()
    write_kingdom_stats()
    # the above displays key kingdom stats - level, control DC, and number of claimed hexes
    startrow = 7
    # the above draws the cells of the skills/attributes table
    hexagon_side_length = 30
    hex_angle = 60
    map_canvas = tk.Canvas(w1, width = 1530, height = 540)
    worldmap = ImageTk.PhotoImage(image1)            
    map_canvas.create_image(0,0,anchor="nw",image=worldmap)
    # the above defines key hex grid parameters, creates the world map window, and places it beside the attribute table
    def draw_hexagon(x=0,y=0,color="black",linewidth=0):
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
                                   width = linewidth)
            start_x = end_x
            start_y = end_y                    
    grid_vertical_offset = -1.4 * hexagon_side_length # parameter to adjust grid position so it matches in-game map
    hex_center_list = []
    def draw_hex_grid():
        # draws a grid of hexagons over the world map. hexagons are drawn starting from the "top" vertex.     
        length = hexagon_side_length # renaming for brevity
        for c in range(30):
            for r in range(13):
                if r % 2 != 0: x_offset = 0.5 * length * sqrt(3)
                else: x_offset = 0                   
                draw_hexagon(x_offset + c * length * sqrt(3), r * length * 1.5 + grid_vertical_offset)
                h = (x_offset + c * length * sqrt(3), length + r * length * 1.5 + grid_vertical_offset)
                hex_center_list.append(h)
    draw_hex_grid()
    # def draw_hex_centers():
        # test function, not useful for main app
        # for (x,y) in hex_center_list:
        #     map_canvas.create_oval(x-5,y-5,x+5,y+5)
    # draw_hex_centers()
    def right_click_add_hex(event=None):
        # add a hex to kingdom.claimed_hexes on right click and draw a red border around the newly claimed hex
        mouse_x, mouse_y = event.x, event.y
        nearest_hex_center = (0,0)
        nearest_hex_distance = 5000
        for (hex_x, hex_y) in hex_center_list:
            distance = sqrt((mouse_x - hex_x)**2 + (mouse_y - hex_y)**2)
            if distance < nearest_hex_distance:
                nearest_hex_center = (hex_x,hex_y)
                nearest_hex_distance = distance
        adjusted_hex_coordinate = (nearest_hex_center[0], nearest_hex_center[1] - hexagon_side_length)
        kingdom.add_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
        draw_kingdom_borders()
        write_kingdom_stats()   
    def middle_click_remove_hex(event=None):
        # remove a claimed hex on middle-click and redraw the world map to remove red border around the lost hex
        mouse_x, mouse_y = event.x, event.y
        nearest_hex_center = (0,0)
        nearest_hex_distance = 5000
        for (hex_x, hex_y) in hex_center_list:
            distance = sqrt((mouse_x - hex_x)**2 + (mouse_y - hex_y)**2)
            if distance < nearest_hex_distance:
                nearest_hex_center = (hex_x,hex_y)
                nearest_hex_distance = distance
        adjusted_hex_coordinate = (nearest_hex_center[0], nearest_hex_center[1] - hexagon_side_length)
        kingdom.remove_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
        map_canvas.delete("all") # horrible hacky strategy: update map by deleting it and redrawing everything
        map_canvas.create_image(0,0,anchor="nw",image=worldmap)
        draw_hex_grid()
        draw_kingdom_borders()
        write_kingdom_stats() 
    map_canvas.bind("<Button-3>", right_click_add_hex)
    map_canvas.bind("<Button-2>", middle_click_remove_hex)    
    def draw_kingdom_borders():
        # draw a thick red border around all hexes claimed by kingdom
        map_canvas.delete("all")
        map_canvas.create_image(0,0,anchor="nw",image=worldmap)
        draw_hex_grid()
        for (x,y) in kingdom.claimed_hexes:
            draw_hexagon(x, y, "red", 2)
    draw_kingdom_borders()
    map_canvas.grid(row = 4, column = 0, rowspan = 30, columnspan = 300)
    # the above adds the world map image, draws the hex grid, and controls addition/removal of kingdom hexes
    def increase_skill(skill,row,column):
        kingdom.increase_skill(skill)
        proficiency_value = tk.Label(w1, text = kingdom.get_modifier(skill))
        proficiency_value.grid(row = row, column = column+1)
    def reduce_skill(skill,row,column):
        kingdom.reduce_skill(skill)
        proficiency_value = tk.Label(w1, text = kingdom.get_modifier(skill))
        proficiency_value.grid(row = row, column = column+1)
    def increase_attribute(attribute,row,column):
        kingdom.increase_attribute(attribute)
        attribute_value = tk.Label(w1, text = kingdom.attributes[attribute])
        attribute_value.grid(row = row, column = column, rowspan = 4, pady = 2)
        update_skills(attribute,row,column-4)
    def reduce_attribute(attribute,row,column):            
        kingdom.reduce_attribute(attribute)
        attribute_value = tk.Label(w1, text = kingdom.attributes[attribute])
        attribute_value.grid(row = row, column = column, rowspan = 4, pady = 2)
        update_skills(attribute,row,column-4)
    def update_skills(attribute, row, col):
        for skill in Kingdom_skills.keys():
            if attribute == Kingdom_skills[skill]:
                skill_label = tk.Label(w1, text = skill.title())
                proficiency_value = tk.Label(w1, text = kingdom.get_modifier(skill))
                skill_label.grid(row = row, column = col+8)
                proficiency_value.grid(row = row, column = col + 9)
                increase_button = tk.Button(w1,text = "^",
                                            command = lambda s = skill, r = row, c = col+8:increase_skill(s,r,c))
                increase_button.grid(row = row, column = col + 10)
                reduce_button = tk.Button(w1,text = "v",
                                            command = lambda s = skill, r = row, c = col+8:reduce_skill(s,r,c))
                reduce_button.grid(row = row, column = col + 11)
                row += 1
    # the above functions are used to draw and update the kingdom attributes/skills/advisors table
    def draw_attribute_table():
        # draws the table of attributes with the associated advisors and skills
        table_startrow = 38
        advisor_startrow = table_startrow
        table_startcol = 0
        horizontal_separator1 = Separator(w1, orient="horizontal")        
        horizontal_separator2 = Separator(w1, orient="horizontal")
        horizontal_separator1.grid(column=table_startcol, row=table_startrow-3, columnspan=66, sticky="ew")
        horizontal_separator2.grid(column=table_startcol, row=table_startrow-1, columnspan=66, sticky="ew")
        for attribute in ["loyalty","stability","culture","economy"]:
            advisor_header = tk.Label(w1,text = "Advisors")
            advisor_header.grid(column=table_startcol, row=table_startrow-2, columnspan=2)
            attribute_header = tk.Label(w1, text = "Attribute")
            attribute_header.grid(column = table_startcol+3, row=table_startrow-2, columnspan=3)
            skill_header = tk.Label(w1, text="Skill")
            skill_header.grid(column=table_startcol+7, row = table_startrow-2, columnspan=3)
            attribute_label = tk.Label(w1, text = attribute.title())
            attribute_label.grid(row = table_startrow, column = table_startcol+3, rowspan = 4)
            attribute_value = tk.Label(w1, text = str(kingdom.attributes[attribute]))
            attribute_value.grid(row = table_startrow, column = table_startcol+4, rowspan = 4)
            increase_button = tk.Button(w1,text = "^",
                                        command = lambda a = attribute, r = table_startrow,
                                        c = table_startcol+4:increase_attribute(a,r,c))
            increase_button.grid(row = table_startrow, column = table_startcol+5, rowspan = 4)
            reduce_button = tk.Button(w1,text = "v",
                                      command = lambda a = attribute, r = table_startrow,
                                      c=table_startcol+4:reduce_attribute(a,r,c))
            reduce_button.grid(row = table_startrow, column = table_startcol + 6, rowspan = 4)
            vsep2 = Separator(w1, orient="vertical")
            vsep2.grid(column=table_startcol+7, row=table_startrow-2, rowspan = 6, sticky="ns")            
            for advisor in Advisors.keys():
                if Advisors[advisor] == attribute:
                    advisor_label = tk.Label(w1, text = advisor.title())
                    advisor_label.grid(row = advisor_startrow, rowspan = 2, column = table_startcol)
                    advisor_status = tk.Label(w1, text = "Appointed")
                    advisor_status.grid(row = advisor_startrow, rowspan = 2, column = table_startcol+1)
                    vsep1 = Separator(w1, orient="vertical")
                    vsep1.grid(column=table_startcol+2, row=table_startrow-2, rowspan = 6, sticky="ns")
                    advisor_startrow += 2
            update_skills(attribute,table_startrow,table_startcol)
            vertical_separator1 = Separator(w1, orient="vertical")
            vertical_separator1.grid(column=table_startcol+15, row=table_startrow-2, rowspan = 6, sticky="nsew")
            vertical_separator2 = Separator(w1, orient="vertical")
            vertical_separator2.grid(column=table_startcol+16, row=table_startrow-2, rowspan = 6, sticky="nsew")
            table_startcol += 17
            advisor_startrow = table_startrow
    # the above creates the attributes/skills/advisors table
    draw_attribute_table() # finally we draw the table!
    ### the code below creates the settlement summary table below the main kingdom map
    def draw_settlements_table():
        col = 40
        settlements_label = tk.Label(w1, text = "Settlements:")
        settlements_label.grid(row = 35, rowspan = 3, column = col-1)
        for settlement in kingdom.settlements:
            name = tk.Label(w1, text = settlement.name.title())
            consumption = tk.Label(w1, text = "Consumption: " + str(settlement.get_consumption()))
            if settlement.is_overcrowded(): crowded = tk.Label(w1, text = "Overcrowded!")
            else: crowded = tk.Label(w1, text = "Not Overcrowded")
            name.grid(row = 35, column = col)
            consumption.grid(row = 36, column = col)
            crowded.grid(row = 37, column = col,sticky="n")
            col += 3
    # draw_settlements_table()
    def draw_problem_table():
        # draws the table of unrest and ruins
        table_startrow = startrow + 25
        unrest_label = tk.Label(w1,text = "Unrest:")
        unrest_label.grid(row=table_startrow, column = 0, sticky="w")
        unrest_value = tk.Label(w1,text=str(kingdom.unrest))
        unrest_value.grid(row=table_startrow, column = 1)
        table_startrow += 1
        for ruin in Ruins:
            ruin_label = tk.Label(w1,text = ruin.title() + ":")
            ruin_label.grid(row=table_startrow, column = 0, sticky="w")
            ruin_value = tk.Label(w1, text = str(kingdom.ruins[ruin]))
            ruin_value.grid(row=table_startrow, column = 1)
            table_startrow += 1
    # draw_problem_table()
    def draw_RP_table():
        # draws the table of kingdom resources - food, lumber, stone, ore, and luxuries
        table_startrow = startrow + 25
        current_RP_label = tk.Label(w1, text="Current RP:")
        current_RP_label.grid(row = table_startrow, column = 4, sticky="w")
        current_RP_value = tk.Label(w1, text = str(kingdom.RP[0]))
        current_RP_value.grid(row = table_startrow, column = 6)
        RP_dice_size_label = tk.Label(w1, text = "Resource dice:")
        RP_dice_size_label.grid(row=table_startrow+1, column = 4,sticky="w",columnspan=2)
        RP_dice_size = tk.Label(w1, text="d" + str(kingdom.RP[1]))
        RP_dice_size.grid(row=table_startrow+1, column = 6)
        next_turn_label = tk.Label(w1, text = "Dice to roll:")
        next_turn_label.grid(row = table_startrow+2, column = 4, columnspan = 2, sticky="w")
        next_turn_value = tk.Label(w1, text = kingdom.RP[2])
        next_turn_value.grid(row = table_startrow+2, column = 6)
    # draw_RP_table()
    blank_space2 = tk.Label(w1, text="")
    blank_space2.grid(row = startrow+32, column = 0, columnspan=13)
    def draw_resource_table():
        table_startrow = startrow + 35
        name_header = tk.Label(w1, text = "Resource")
        amount_header = tk.Label(w1,text = "Stored \n Amount")
        capacity_header = tk.Label(w1,text="Storage \n Capacity")
        gain_header = tk.Label(w1,text="Next \n Turn")
        name_header.grid(row=table_startrow, column=0)
        amount_header.grid(row=table_startrow, column=1,columnspan=2)
        capacity_header.grid(row=table_startrow, column=3, columnspan=3)
        gain_header.grid(row=table_startrow, column=6, columnspan=3)
        for resource in kingdom.resources.keys():
            resource_label = tk.Label(w1, text = resource.title())
            current = tk.Label(w1,text=kingdom.resources[resource][0])
            capacity = tk.Label(w1,text=kingdom.resources[resource][1])
            next_turn = tk.Label(w1,text=kingdom.resources[resource][2])
    # draw_resource_table()
    w1.mainloop()