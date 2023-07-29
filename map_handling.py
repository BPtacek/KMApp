# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:57:40 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from math import cos, sin, sqrt, radians
from settlements_tab import *

# the above defines key hex grid parameters and creates the world map canvas
def draw_hexagon(state,x=0, y=0, color="black", linewidth=0):
    # draws a single hexagon
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
    # draws a grid of hexagons over the world map. hexagons are drawn starting from the "top" vertex.     
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
    # returns the pixel coordinates of the top vertex of the grid hex where the mouse was clicked
    nearest_hex_center = (0, 0)
    nearest_hex_distance = 5000
    for (hex_x, hex_y) in state.hex_center_list:
        distance = sqrt((mouse_x - hex_x) ** 2 + (mouse_y - hex_y) ** 2)
        if distance < nearest_hex_distance:
            nearest_hex_center = (hex_x, hex_y)
            nearest_hex_distance = distance
    return (nearest_hex_center[0], nearest_hex_center[1] - state.hexagon_side_length)

def left_click_add_hex(x,y,state):
    # add a hex to kingdom.claimed_hexes on right click and draw a red border around the newly claimed hex
    adjusted_hex_coordinate = identify_hex(x,y,state)
    state.kingdom.add_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
    draw_kingdom_borders(state)

def middle_click_remove_hex(x,y,state):
    # remove a claimed hex on middle-click and redraw the world map to remove red border around the lost hex
    adjusted_hex_coordinate = identify_hex(x, y, state)
    state.kingdom.remove_hex((adjusted_hex_coordinate[0], adjusted_hex_coordinate[1]))
    state.map_canvas.delete("all")  # horrible hacky strategy: update map by deleting it and redrawing everything
    state.map_canvas.create_image(0, 0, anchor="nw", image=state.worldmap)
    draw_hex_grid(state)
    draw_kingdom_borders(state)

def menu_add_settlement(x,y,state):
    kingdom = state.kingdom
    top = tk.Toplevel(state.map_canvas)
    label = tk.Label(top,text="New Settlement Name:")
    label.grid(row=0,column=0)
    new_name=tk.StringVar(top,value="")
    entry = tk.Entry(top,width=25,textvariable=new_name)
    entry.grid(row=0,column=1)
    def name_listener(event=None):
        name = entry.get()        
        kingdom.add_settlement(name,(x,y),{})        
        state.destroy_table_frame("settlements frame")
        state.destroy_table_frame("settlement buildings frame")
        draw_buildings_and_settlements_tables(state)
        top.destroy()
    entry.bind("<Return>",name_listener)    

def right_click_menu(x,y,state):
    m = tk.Menu(state.map_canvas,tearoff=0)
    (hex_x,hex_y) = (x,y)
    m.add_command(label="Add Settlement",command = lambda s=state,x=x,y=y:menu_add_settlement(x,y,s))
    m.add_command(label="Add Farm")
    m.add_command(label="Add Lumber Camp")
    m.add_command(label="Add Mine")
    m.add_command(label="Add Quarry")
    m.add_command(label="Add Road")    
    m.tk_popup(x,y)    

def draw_kingdom_borders(state):
    # draw a thick red line over the hex grid around the kingdom's external borders
    kingdom = state.kingdom
    length = state.hexagon_side_length
    angle = state.hex_angle
    canvas = state.map_canvas
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=state.worldmap)    
    draw_hex_grid(state)
    linepoints1 = []
    def truncate(a): # a is a float; discard everything after first 5 decimal places
        return float(f'{a:.5f}')
    for (x, y) in kingdom.claimed_hexes:
        start_x = x
        start_y = y            
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
            canvas.create_line(x1,y1,x2,y2,fill="red",width=3)                
