# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:57:40 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
from math import cos, sin, sqrt, radians
from PIL import ImageTk, Image
from settlements_tab import *

# the above defines key hex grid parameters and creates the world map canvas
def draw_hexagon(state,x=0, y=0, color="black", linewidth=0):
    """draws a single hexagon"""
    length = state.hexagon_side_length
    angle = state.hex_angle
    start_x = x
    start_y = y
    for i in range(6):
        end_x = start_x + length * cos(radians(30 + angle * i))
        end_y = start_y + length * sin(radians(30 + angle * i))
        state.map_canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=linewidth)
        start_x = end_x
        start_y = end_y

def draw_hex_grid(state):
    """"draws a grid of hexagons over the world map. hexagons are drawn starting from the 'top' vertex."""     
    length = state.hexagon_side_length  # renaming for brevity
    grid_vertical_offset = -1.4 * length  # parameter to adjust grid position so it matches in-game map
    for c in range(30):
        for r in range(13):
            if r % 2 != 0:
                x_offset = 0.5 * length * sqrt(3)
            else:
                x_offset = 0
            draw_hexagon(state, x_offset + c * length * sqrt(3), r * length * 1.5 + grid_vertical_offset)
            h = (x_offset + c * length * sqrt(3), length + r * length * 1.5 + grid_vertical_offset)
            state.add_to_hex_center_list(h)

def identify_hex(mouse_x, mouse_y, state):
    """returns the pixel coordinates of the top vertex of the grid hex where the mouse was clicked"""
    nearest_hex_center = (0, 0)
    nearest_hex_distance = 5000
    for (hex_x, hex_y) in state.hex_center_list:
        distance = sqrt((mouse_x - hex_x) ** 2 + (mouse_y - hex_y) ** 2)
        if distance < nearest_hex_distance:
            nearest_hex_center = (hex_x, hex_y)
            nearest_hex_distance = distance
    return (nearest_hex_center[0], nearest_hex_center[1] - state.hexagon_side_length)

def left_click_add_hex(x,y,state):
    """add a hex to kingdom.claimed_hexes on right click and draw a red border around the newly claimed hex"""
    adjusted_hex_coordinate = identify_hex(x,y,state)
    state.kingdom.add_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
    draw_kingdom_borders(state)

def middle_click_remove_hex(x,y,state):
    """remove a claimed hex on middle-click and redraw the world map to remove red border around the lost hex"""
    adjusted_hex_coordinate = identify_hex(x, y, state)
    state.kingdom.remove_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
    draw_kingdom_borders(state)

def menu_add_settlement(x,y,state):
    """Context menu function to add a new settlement to the kingdom"""
    kingdom = state.kingdom
    top = tk.Toplevel(state.map_canvas)
    label = tk.Label(top,text="New Settlement Name:")
    label.grid(row=0,column=0)
    new_name=tk.StringVar(top,value="")
    entry = tk.Entry(top,width=25,textvariable=new_name)
    entry.grid(row=0,column=1)
    (center_x,center_y) = identify_hex(x,y,state)
    def name_listener(event=None):        
        name = entry.get()        
        kingdom.add_settlement(name,(center_x,center_y),{})        
        state.destroy_table_frame("settlements frame")
        state.destroy_table_frame("settlement buildings frame")
        draw_kingdom_borders(state)
        draw_buildings_and_settlements_tables(state)
        top.destroy()
    entry.bind("<Return>",name_listener)    
    
def toggle_explored(x,y,state):
    """Context menu function to toggle a hex between explored and unexplored states"""
    (x,y) = identify_hex(x,y,state)
    if (x,y) in state.kingdom.explored_hexes:
        state.kingdom.remove_explored_hex((x,y))
        draw_kingdom_borders(state) 
    else:        
        state.kingdom.add_explored_hex((x,y))
        draw_kingdom_borders(state)
        
def add_jobsite(x,y,state,name):
    """Context menu function to add a logging camp/farm/quarry/mine to the chosen hex"""
    (x,y) = identify_hex(x,y,state)
    if (x,y) in state.kingdom.claimed_hexes and (x,y) not in state.kingdom.work_camps[name]:
        state.kingdom.add_work_site((x,y),name)
        state.update_stringvars()
        draw_kingdom_borders(state)
        
def add_road(x,y,state):
    """Context menu function to add a road to the chosen hex"""
    coordinates = identify_hex(x,y,state)
    state.kingdom.add_road(coordinates)
    draw_kingdom_borders(state)

def draw_roads(state):
    """Context menu function to draw the kingdom's road network"""
    kingdom = state.kingdom
    index = len(kingdom.roads)
    length = state.hexagon_side_length
    canvas = state.map_canvas
    road_list = []
    def get_distance(coordinates1,coordinates2):
        return sqrt((coordinates1[0] - coordinates2[0])**2 + (coordinates1[1]-coordinates2[1])**2)
    for i in range(index):
        for j in kingdom.roads[i+1:]:
            if j != []:               
                if get_distance(kingdom.roads[i],j) <= 1 + length * sqrt(3):
                    startpoint = (kingdom.roads[i][0], length + kingdom.roads[i][1])
                    endpoint = (j[0],length+j[1])
                    road_list.append((startpoint,endpoint))
    for (start,end) in road_list:
        canvas.create_line(start[0],start[1],end[0],end[1],fill="gray",width=4)
        # print("Tried to add road between " + str(start) + " and " + str(end))
        # print(roadlist)
            
def right_click_menu(x,y,x_root,y_root,state):
    """Creates the right-click context menu for the map tab"""
    m = tk.Menu(state.map_canvas,tearoff=0)
    (hex_x,hex_y) = (x,y)
    m.add_command(label="Add Settlement",command = lambda s=state,x=x,y=y:menu_add_settlement(x,y,s))
    m.add_command(label="Add Farm",command=lambda s=state,x=x,y=y:add_jobsite(x,y,s,"Farms"))
    m.add_command(label="Add Lumber Camp",command=lambda s=state,x=x,y=y:add_jobsite(x,y,s,"Logging Camps"))
    m.add_command(label="Add Mine",command=lambda s=state,x=x,y=y:add_jobsite(x,y,s,"Mines"))
    m.add_command(label="Add Quarry",command=lambda s=state,x=x,y=y:add_jobsite(x,y,s,"Quarries"))
    m.add_command(label="Add Road",command=lambda s=state,x=x,y=y:add_road(x,y,s))
    m.add_command(label="Toggle Explored State",command = lambda s=state,x=x,y=y:toggle_explored(x,y,s))  
    m.tk_popup(x_root,y_root)       

def place_map_icons(state):
    """Draws icons or shapes on the map to represent settlements, work camps, and roads"""
    kingdom = state.kingdom
    canvas = state.map_canvas
    length = state.hexagon_side_length
    wheat = Image.open("Images/bigwheat.png")  
    # farm_icon = ImageTk.PhotoImage(wheat)    
    for settlement in kingdom.settlements:
        (x,y) = (settlement.location[0],settlement.location[1]+length)
        canvas.create_oval(x-10,y-10,x+10,y+10,fill="blue")
    for mine in kingdom.work_camps["Mines"]:
        (x,y) = (mine[0],mine[1]+length)
        canvas.create_oval(x-8,y-8,x+8,y+8,fill="red")
    for logging_camp in kingdom.work_camps["Logging Camps"]:
        (x,y) = (logging_camp[0],logging_camp[1]+length)
        canvas.create_oval(x-8,y-8,x+8,y+8,fill="yellow")
    for quarry in kingdom.work_camps["Quarries"]:
        (x,y) = (quarry[0],quarry[1]+length)
        canvas.create_oval(x-8,y-8,x+8,y+8,fill="black")
    for farm in kingdom.work_camps["Farms"]:
        (x,y) = (farm[0],farm[1]+length)
        canvas.create_oval(x-8,y-8,x+8,y+8,fill="green")
        # canvas.create_image(x,y,anchor="nw",image=farm_icon)

def draw_kingdom_borders(state):
    """draw a thick red line over the hex grid around the kingdom's external borders and a dashed red line
    around the explored hexes, and then places settlements, roads, and work camps"""
    kingdom = state.kingdom
    length = state.hexagon_side_length
    angle = state.hex_angle
    canvas = state.map_canvas
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=state.worldmap)    
    draw_hex_grid(state)
    draw_roads(state)
    def truncate(a): # a is a float; discard everything after first 5 decimal places
        return float(f'{a:.5f}')
    def set_border_coordinates(coordinate_list,exclusion_list=[]):
        lp = []
        for (x, y) in coordinate_list:
            start_x = x
            start_y = y            
            for i in range(6):
                end_x = start_x + length * cos(radians(30 + angle * i))
                end_y = start_y + length * sin(radians(30 + angle * i))
                x1 = truncate(start_x)
                x2 = truncate(end_x)
                y1 = truncate(start_y)
                y2 = truncate(end_y)
                lp.append(((x1,y1),(x2,y2)))
                start_x = end_x
                start_y = end_y
        return [(start,end) for (start,end) in lp if ((end,start) not in lp) and ((start,end) not in exclusion_list)]
    claimed_border = set_border_coordinates(kingdom.claimed_hexes)
    explored_border = set_border_coordinates(kingdom.explored_hexes,claimed_border)
    for (start,end) in claimed_border:
        canvas.create_line(start[0],start[1],end[0],end[1],fill="red",width=3)
    for (start,end) in explored_border:
        canvas.create_line(start[0],start[1],end[0],end[1],fill="red",width=3,dash=(5,2))    
    place_map_icons(state)
