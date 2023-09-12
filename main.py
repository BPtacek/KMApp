# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 20:41:37 2023

@author: dtbla
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from math import cos, sin, sqrt, radians
from PIL import ImageTk, Image

# from buildings import *
from nethysparse import *
from file_handling import *
from map_handling import *
from details_tab import *
from settlements_tab import *
from activities import *

w1 = tk.Tk()
w1.title("Kingdom Management!")

kingdom=Kingdom(name="Unnamed Kingdom")

attribute_variables = {i:tk.IntVar(w1,value=kingdom.get_attribute(i)) for i in attributes}
skill_modifiers = {i:tk.IntVar(w1,value=kingdom.get_skill_modifier(i)) for i in Kingdom_skills.keys()}
proficiency_variables = {i:tk.StringVar(w1) for i in Kingdom_skills.keys()}
ruin_variables = {i:tk.StringVar(w1,value=kingdom.ruins[i]) for i in Ruins}
site_numbers = {i:tk.StringVar(w1,value="0") for i in resources_jobsites.values()}

initial_state = State(kingdom=kingdom,attribute_variables=attribute_variables,skill_modifiers=skill_modifiers,
                  proficiency_variables=proficiency_variables,ruin_variables=ruin_variables,
                  site_numbers=site_numbers)

def draw_tables(state):
    state.clear_all_tabs()
    create_headline_structure(state)
    create_canvas(state)
    state.update_stringvars()
    draw_kingdom_borders(state)
    draw_attribute_overview(state)
    draw_attribute_details(state)   
    draw_name_table(state)   
    draw_level_table(state)
    draw_resource_table(state)    
    draw_unrest_table(state)
    draw_ruins_table(state)       
    draw_buildings_and_settlements_tables(state)
    building_search_table(state)
    state.write_headline_stats()
    draw_name_table(state)
    activity_search_table(state)

def new_kingdom(state):
    state.kingdom.reset()
    draw_tables(state)

def save_file(state):
    export_kingdom_as_file(state.kingdom)

def open_file(state):
    read_json(state.kingdom)
    draw_tables(state)
    
menubar = tk.Menu(w1)    
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New...", command=lambda s = initial_state: new_kingdom(s))
filemenu.add_command(label="Open", command=lambda s = initial_state: open_file(s))
filemenu.add_command(label="Save", command=lambda s = initial_state: save_file(s))
# filemenu.add_command(label="Save As", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=w1.destroy)
menubar.add_cascade(label="File", menu=filemenu)
w1.config(menu=menubar)

def create_tabs(state):
    if state.tabs != {}:
        for (name,tab) in state.tabs.items():
            state.tabs[name] = None
            tab.destroy()
    tabControl = ttk.Notebook(w1)
    kingdom_overview = ttk.Frame(tabControl)
    kingdom_details = ttk.Frame(tabControl)
    settlements_tab = ttk.Frame(tabControl)    
    feats_tab = ttk.Frame(tabControl)    
    activities_tab = ttk.Frame(tabControl)    
    tabControl.add(kingdom_overview, text="Kingdom Overview")
    tabControl.add(kingdom_details, text="Kingdom Details")
    tabControl.add(settlements_tab, text="Settlements & Buildings")       
    tabControl.add(feats_tab, text="Kingdom Feats")       
    tabControl.add(activities_tab, text="Kingdom Activities")       
    tabControl.grid(row=1, column=0, columnspan=5000)    
    tabs = {"overview":kingdom_overview,
            "details":kingdom_details,
            "settlements":settlements_tab,
            "feats":feats_tab,
            "activities":activities_tab}
    state.set_tabs(tabs)

def create_headline_structure(state):
    # create the three headline frames for each tab to dislay key kingdoms stats and link them to 
    # a dictionary of global variables so they can be destroyed rather than overwritten
    if state.main_header !=  "placeholder":
        state.main_header.destroy()
    main_header = tk.Frame(w1)
    kname = tk.StringVar(main_header,value=state.kingdom.name)
    state.set_name_stringvar(kname)
    header = tk.Label(main_header, textvariable=kname)
    header.grid(row=0,column=0)
    main_header.grid(row=0,column=0,columnspan=5000)
    state.set_main_header(main_header)
    #################################
    tabs = state.tabs
    headline_frames = {}
    index = 0
    for (name,tab) in tabs.items():
        top_separator = ttk.Separator(tab, orient="horizontal")
        top_separator.grid(column=0, row=0, columnspan=20, sticky="ew")
        headline_frames[name] = tk.Frame(tab)
        headline_frames[name].grid(row=1,column=0,columnspan=20)        
        bottom_separator = ttk.Separator(tab, orient="horizontal")
        bottom_separator.grid(column=0, row=2, columnspan=20, sticky="ew")
        index += 1
    state.assign_headline_frames(headline_frames)
     
# the above displays the headline kingdom stats shown at the top of every tab:
# level, control DC, number of claimed hexes, unrest, food status, ruins

def create_canvas(state):
    image1 = Image.open("Images/GridlessMap75.jpeg")  
    map_canvas = tk.Canvas(state.tabs["overview"], width=1530, height=540)
    map_canvas.grid(row=4, column=0, rowspan=30, columnspan=300)
    state.set_map_canvas(map_canvas)
    worldmap = ImageTk.PhotoImage(image1)
    state.set_worldmap(worldmap)
    state.map_canvas.create_image(0, 0, anchor="nw", image=state.worldmap)
    
    def lclick(event=None,state=state):
        (x,y) = (event.x,event.y)
        left_click_add_hex(x,y,state)
        state.write_headline_stats()
        
    def mclick(event=None,state=state):
        (x,y) = (event.x,event.y)
        middle_click_remove_hex(x,y,state)
        state.write_headline_stats()
        
    def rclick(event=None,state=state):
        (x,y,x_root,y_root) = (event.x,event.y,event.x_root,event.y_root)
        right_click_menu(x,y,x_root,y_root,state)
    
    state.map_canvas.bind("<Button-1>", lclick)
    state.map_canvas.bind("<Button-2>", mclick)
    state.map_canvas.bind("<Button-3>", rclick)

create_tabs(initial_state)
draw_tables(initial_state)

w1.mainloop()
