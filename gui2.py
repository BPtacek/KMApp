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

Noktown = Settlement("Noktown", (1013.2497224277931, 273.0), 2,
                     {Houses: 2, GeneralStore: 1, TownHall: 1, AlchemyLab: 1, Mill: 1, PopularTavern: 1, WoodenWall: 1})
Lizards = Settlement("Isle of the Lizard King", (909.3266739736605, 363.0), 1, {Houses: 1, Mill: 1, Shrine: 1})
Tatzlford = Settlement("Tatzlford", (883.3459118601273, 228.0), 2,
                       {Houses: 1, TownHall: 1, Inn: 1, Orphanage: 1, Barracks: 1})
Greenbelt = Kingdom("Greenbelt Republic", [],
                    5, 0, {i: 0 for i in Ruins}, [Noktown, Lizards, Tatzlford],
                    {"culture": 14, "economy": 16, "loyalty": 14, "stability": 14},
                    {i: 0 for i in Kingdom_skills.keys()},
                    {i: "filled" for i in Advisors.keys()}, {}, [30, 6, 13], {"food": [5, 8, 2]})

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
    
    tabControl = ttk.Notebook(w1)
    kingdom_overview = ttk.Frame(tabControl)
    settlements_tab = ttk.Frame(tabControl)
    feats_tab = ttk.Frame(tabControl)
    tabControl.add(kingdom_overview, text="Kingdom Overview")
    tabControl.add(settlements_tab, text="Settlements")
    tabControl.add(feats_tab, text="Kingdom Feats")
    tabControl.pack(expand=1, fill="both")
    
    header = tk.Label(kingdom_overview, text=kingdom.name + " Kingdom Overview")
    header.grid(row=0, column=0, pady=2, padx=2, columnspan=5000)
    header_separator = ttk.Separator(kingdom_overview, orient="horizontal")
    header_separator.grid(column=0, row=1, columnspan=5000, sticky="ew")

    # the above creates the app header
    def write_kingdom_stats():
        header_frame = tk.Frame(kingdom_overview)
        header_frame.grid(row=2, column=0, columnspan=80)
        level_frame = tk.Frame(header_frame)
        level_label = tk.Label(level_frame, text="Level: " + str(kingdom.level))
        increase_button = tk.Button(level_frame, text="^", command=lambda: increase_level())
        reduce_button = tk.Button(level_frame, text="v", command=lambda: reduce_level())
        level_label.grid(row=0, column=0)
        increase_button.grid(row=0, column=1)
        reduce_button.grid(row=0, column=2)
        level_frame.grid(row=0, column=0, padx=10)
        control_label = tk.Label(header_frame, text="Control DC: " + str(kingdom.control_DC))
        control_label.grid(row=0, column=1, padx=10)
        hexes_label = tk.Label(header_frame, text="Claimed Hexes: " + str(len(kingdom.claimed_hexes)))
        hexes_label.grid(row=0, column=3, padx=10)
        unrest_label = tk.Label(header_frame, text="Unrest: " + str(kingdom.unrest))
        unrest_label.grid(row=0, column=4, padx=10)
        food_label = tk.Label(header_frame, text="Food: " + str(kingdom.resources["food"][0]))
        food_label.grid(row=0, column=5, padx=10)
        food_capacity_label = tk.Label(header_frame, text="Food Consumed/Turn: " + str(kingdom.get_consumption()))
        food_capacity_label.grid(row=0, column=6, padx=10)
        food_turn_label = tk.Label(header_frame, text="Food Gained/Turn: " + str(kingdom.resources["food"][2]))
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

    # def draw_hex_centers():
    # test function, not useful for main app
    # for (x,y) in hex_center_list:
    #     map_canvas.create_oval(x-5,y-5,x+5,y+5)
    # draw_hex_centers()
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
        write_kingdom_stats()

    def middle_click_remove_hex(event=None):
        # remove a claimed hex on middle-click and redraw the world map to remove red border around the lost hex
        adjusted_hex_coordinate = identify_hex(event.x, event.y)
        kingdom.remove_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
        map_canvas.delete("all")  # horrible hacky strategy: update map by deleting it and redrawing everything
        map_canvas.create_image(0, 0, anchor="nw", image=worldmap)
        draw_hex_grid()
        draw_kingdom_borders()
        write_kingdom_stats()

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
    def increase_skill(skill, row, column):
        kingdom.increase_skill(skill)
        proficiency_value = tk.Label(kingdom_overview, text=kingdom.get_modifier(skill))
        proficiency_value.grid(row=row, column=column + 1)

    def reduce_skill(skill, row, column):
        kingdom.reduce_skill(skill)
        proficiency_value = tk.Label(kingdom_overview, text=kingdom.get_modifier(skill))
        proficiency_value.grid(row=row, column=column + 1)

    def increase_attribute(attribute, row, column):
        kingdom.increase_attribute(attribute)
        attribute_value = tk.Label(kingdom_overview, text=kingdom.attributes[attribute])
        attribute_value.grid(row=row, column=column, rowspan=4, pady=2)
        update_skills(attribute, row, column - 4)

    def reduce_attribute(attribute, row, column):
        kingdom.reduce_attribute(attribute)
        attribute_value = tk.Label(kingdom_overview, text=kingdom.attributes[attribute])
        attribute_value.grid(row=row, column=column, rowspan=4, pady=2)
        update_skills(attribute, row, column - 4)

    def update_skills(attribute, row, col):
        for skill in Kingdom_skills.keys():
            if attribute == Kingdom_skills[skill]:
                skill_label = tk.Label(kingdom_overview, text=skill.title())
                proficiency_value = tk.Label(kingdom_overview, text=kingdom.get_modifier(skill))
                skill_label.grid(row=row, column=col + 8)
                proficiency_value.grid(row=row, column=col + 9)
                increase_button = tk.Button(kingdom_overview, text="^",
                                            command=lambda s=skill, r=row, c=col + 8: increase_skill(s, r, c))
                increase_button.grid(row=row, column=col + 10)
                reduce_button = tk.Button(kingdom_overview, text="v",
                                          command=lambda s=skill, r=row, c=col + 8: reduce_skill(s, r, c))
                reduce_button.grid(row=row, column=col + 11)
                row += 1

    # the above functions are used to draw and update the kingdom attributes/skills/advisors table
    def draw_attribute_table():
        # draws the table of attributes with the associated advisors and skills
        table_startrow = 38
        advisor_startrow = table_startrow
        table_startcol = 0
        horizontal_separator1 = ttk.Separator(kingdom_overview, orient="horizontal")
        horizontal_separator2 = ttk.Separator(kingdom_overview, orient="horizontal")
        horizontal_separator1.grid(column=table_startcol, row=table_startrow - 3, columnspan=66, sticky="ew")
        horizontal_separator2.grid(column=table_startcol, row=table_startrow - 1, columnspan=66, sticky="ew")
        for attribute in ["loyalty", "stability", "culture", "economy"]:
            advisor_header = tk.Label(kingdom_overview, text="Advisors")
            advisor_header.grid(column=table_startcol, row=table_startrow - 2, columnspan=2)
            attribute_header = tk.Label(kingdom_overview, text="Attribute")
            attribute_header.grid(column=table_startcol + 3, row=table_startrow - 2, columnspan=3)
            skill_header = tk.Label(kingdom_overview, text="Skill")
            skill_header.grid(column=table_startcol + 7, row=table_startrow - 2, columnspan=3)
            attribute_label = tk.Label(kingdom_overview, text=attribute.title())
            attribute_label.grid(row=table_startrow, column=table_startcol + 3, rowspan=4)
            attribute_value = tk.Label(kingdom_overview, text=str(kingdom.attributes[attribute]))
            attribute_value.grid(row=table_startrow, column=table_startcol + 4, rowspan=4)
            increase_button = tk.Button(kingdom_overview, text="^", command=lambda a=attribute, r=table_startrow,
                                                                     c=table_startcol + 4: increase_attribute(a, r, c))
            increase_button.grid(row=table_startrow, column=table_startcol + 5, rowspan=4)
            reduce_button = tk.Button(kingdom_overview, text="v", command=lambda a=attribute, r=table_startrow,
                                                                   c=table_startcol + 4: reduce_attribute(a, r, c))
            reduce_button.grid(row=table_startrow, column=table_startcol + 6, rowspan=4)
            vsep2 = ttk.Separator(kingdom_overview, orient="vertical")
            vsep2.grid(column=table_startcol + 7, row=table_startrow - 2, rowspan=6, sticky="ns")
            for advisor in Advisors.keys():
                if Advisors[advisor] == attribute:
                    advisor_label = tk.Label(kingdom_overview, text=advisor.title())
                    advisor_label.grid(row=advisor_startrow, rowspan=2, column=table_startcol)
                    advisor_status = tk.Label(kingdom_overview, text="Appointed")
                    advisor_status.grid(row=advisor_startrow, rowspan=2, column=table_startcol + 1)
                    vsep1 = ttk.Separator(kingdom_overview, orient="vertical")
                    vsep1.grid(column=table_startcol + 2, row=table_startrow - 2, rowspan=6, sticky="ns")
                    advisor_startrow += 2
            update_skills(attribute, table_startrow, table_startcol)
            vertical_separator1 = ttk.Separator(kingdom_overview, orient="vertical")
            vertical_separator1.grid(column=table_startcol + 15, row=table_startrow - 2, rowspan=6, sticky="nsew")
            vertical_separator2 = ttk.Separator(kingdom_overview, orient="vertical")
            vertical_separator2.grid(column=table_startcol + 16, row=table_startrow - 2, rowspan=6, sticky="nsew")
            table_startcol += 17
            advisor_startrow = table_startrow
    # the above creates the attributes/skills/advisors table
    draw_attribute_table()  # finally we draw the table!
    #
    def export_kingdom_as_file(file_name, kingdom=Greenbelt, print_only=False):
        file_name = file_name if file_name.endswith(".json") else file_name + ".json"
        kingdom_data = kingdom.export_kingdom_data()
        if print_only:
            print(json.dumps(kingdom_data, indent=4))
            return
        with open(f"{file_name}", "w") as f:
            json.dump(kingdom_data, f, indent=4)

    w1.mainloop()
