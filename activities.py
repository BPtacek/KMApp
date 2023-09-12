# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 13:36:25 2023

@author: dtbla
"""
import tkinter as tk
from tkinter import ttk
from nethysparse import *
from constants import *
from skillparse import *

phases = ["Upkeep","Commerce","Leadership","Region","Civic"]

def activity_search_table(state):
    kingdom = state.kingdom    
    activities_tab = state.tabs["activities"]
    checkbox_frame = tk.Frame(activities_tab,borderwidth=1,relief="groove")
    checkbox_frame.grid(row=3,column=3,sticky="n")
    activities_search_frame = tk.Frame(activities_tab,borderwidth=1,relief="groove")
    activities_search_frame.grid(row=3,column=4,sticky="n",padx=20)
    activity_details_frame = tk.Frame(activities_tab, borderwidth=1,relief="groove")
    activity_details_frame.grid(row=3,column=5,sticky="n")
    state.add_table_frame("activities search",activities_search_frame)
    state.add_table_frame("activity details",activity_details_frame)
    activities_canvas = tk.Canvas(activities_search_frame,width=470,height=670)  
    activities_canvas.grid(row=0,column=0)    
    ########### Frame Layout ##############    
    filter_label = tk.Label(checkbox_frame,text="Activity Filters",font=("Segoe UI",10,"bold"))
    filter_label.grid(row=0,column=0,columnspan=2)
    show_only = tk.Label(checkbox_frame,text="Show only activities that:")
    show_only.grid(row=1,column=0,rowspan=5)
    unrest_var = tk.IntVar(checkbox_frame,value=0)
    ruins_var = tk.IntVar(checkbox_frame,value=0)
    comm_var = tk.IntVar(checkbox_frame,value=0)
    rp_var = tk.IntVar(checkbox_frame,value=0)
    food_var = tk.IntVar(checkbox_frame,value=0)
    ######################################
    def activity_list_refresher():
        activity_dict = general_activities
        if unrest_var.get():
            activity_dict = {i:j for (i,j) in activity_dict.items() if j["Reduce Unrest"]}        
        if ruins_var.get():
            activity_dict = {i:j for (i,j) in activity_dict.items() if j["Reduce Ruins"]}
        if comm_var.get():
            activity_dict = {i:j for (i,j) in activity_dict.items() if j["Gain Commodities"]}
        if rp_var.get():
            activity_dict = {i:j for (i,j) in activity_dict.items() if j["Gain RP"]}
        if food_var.get():
            activity_dict = {i:j for (i,j) in activity_dict.items() if j["Gain Food"]}
        draw_activities_list(activity_dict)
    #####################################
    unrest_checkbox = tk.Checkbutton(checkbox_frame,text="Reduce Unrest",variable=unrest_var,onvalue=1,offvalue=0,
                                     command=lambda:activity_list_refresher())
    unrest_checkbox.grid(row=1,column=1,sticky="w")    
    ruins_checkbox = tk.Checkbutton(checkbox_frame,text="Reduce Ruins",variable=ruins_var,onvalue=1,offvalue=0,
                                     command=lambda:activity_list_refresher())
    ruins_checkbox.grid(row=2,column=1,sticky="w")    
    rp_checkbox = tk.Checkbutton(checkbox_frame,text="Increase RP",variable=rp_var,onvalue=1,offvalue=0,
                                     command=lambda:activity_list_refresher())
    rp_checkbox.grid(row=3,column=1,sticky="w")    
    comm_checkbox = tk.Checkbutton(checkbox_frame,text="Provide Commodities",variable=comm_var,onvalue=1,offvalue=0,
                                     command=lambda:activity_list_refresher())
    comm_checkbox.grid(row=4,column=1,sticky="w")    
    food_checkbox = tk.Checkbutton(checkbox_frame,text="Provide Food",variable=food_var,onvalue=1,offvalue=0,
                                     command=lambda:activity_list_refresher())
    food_checkbox.grid(row=5,column=1,sticky="w")
    #######################################
    def show_activity_details(name,details):
        for widget in activity_details_frame.winfo_children():
            widget.destroy()
        current_row=0
        header = tk.Label(activity_details_frame,text=name + " Details",font=("Segoe UI",10,"bold"))
        header.grid(row=current_row,column=0,columnspan=3)
        current_row += 1
        desc_label = tk.Label(activity_details_frame,text="Description:")
        desc_label.grid(row=current_row,column=0,sticky="n")
        desc = tk.Label(activity_details_frame,text=details["Description"],wraplength=550,justify="left")
        desc.grid(row=current_row,column=1,sticky="w",columnspan=2)
        current_row += 1
        if "Requirements" in details.keys():
            reqs_label = tk.Label(activity_details_frame,text="Requirements:")        
            reqs_label.grid(row=current_row,column=0,sticky="n")
            req_text = tk.Label(activity_details_frame,text=details["Requirements"],wraplength=550,justify="left")
            req_text.grid(row=current_row,column=1,sticky="w",columnspan=2)
            current_row += 1
        num_skills = len(details["Skills"])                                
        skills_label = tk.Label(activity_details_frame, text = "Skills:")
        skills_label.grid(column=0,row=current_row,rowspan=max(1,num_skills))
        if details["Skills"] != []:
            for skill in details["Skills"]:
                skill_name = tk.Label(activity_details_frame, text=skill.title())
                skill_name.grid(row=current_row,column=1)
                modifier = kingdom.get_skill_modifier(skill)
                modifier_label = tk.Label(activity_details_frame, text=modifier)
                modifier_label.grid(row=current_row, column=2)
                current_row += 1
        cs_label = tk.Label(activity_details_frame,text="Critical Success:")
        cs_label.grid(row=current_row,column=0,sticky="n")
        crit_success = tk.Label(activity_details_frame,text=details["Critical Success"],wraplength=550,justify="left")
        crit_success.grid(row=current_row,column=1,sticky="w",columnspan=2)
        current_row += 1
        s_label = tk.Label(activity_details_frame,text="Success:")
        s_label.grid(row=current_row,column=0,sticky="n")
        success = tk.Label(activity_details_frame,text=details["Success"],wraplength=550,justify="left")
        success.grid(row=current_row,column=1,sticky="w",columnspan=2)
        current_row += 1
        f_label = tk.Label(activity_details_frame,text="Failure:")
        f_label.grid(row=current_row,column=0,sticky="n")
        failure = tk.Label(activity_details_frame,text=details["Failure"],wraplength=550,justify="left")
        failure.grid(row=current_row,column=1,sticky="w",columnspan=2)
        current_row += 1
        cf_label = tk.Label(activity_details_frame,text="Critical Failure:")
        cf_label.grid(row=current_row,column=0,sticky="n")
        crit_fail = tk.Label(activity_details_frame,text=details["Critical Failure"],wraplength=550,justify="left")
        crit_fail.grid(row=current_row,column=1,sticky="w",columnspan=2)
        current_row += 1
        if "Special" in details.keys():
            special_label = tk.Label(activity_details_frame,text="Special:")
            special_label.grid(row=current_row,column=0,sticky="n")
            special_text = tk.Label(activity_details_frame,text=details["Special"],wraplength=550,justify="left")
            special_text.grid(row=current_row,column=1,sticky="w",columnspan=2)
    ####################
    def draw_activities_list(activity_dict):
        activities_canvas.delete("all")
        inner_frame = tk.Frame(activities_canvas)
        activities_canvas.create_window((0,0), window=inner_frame, anchor="nw")
        current_row = 0
        for phase in phases: 
            phase_activities = {i:j for (i,j) in activity_dict.items() if phase in j["Traits"]}
            sorted_activities = dict(sorted(phase_activities.items()))
            phase_header = tk.Label(inner_frame, text=phase.upper() + " PHASE", font=("Segoe UI",10,"bold"))
            phase_header.grid(column=0, row=current_row, columnspan=5)
            current_row += 1
            bottom_sep = ttk.Separator(inner_frame, orient="horizontal")
            bottom_sep.grid(column=0, columnspan=5, row=current_row, sticky="ew")
            current_row += 1
            for (name,details) in sorted_activities.items():
                activity_name = tk.Label(inner_frame, text=name,font=("Segoe UI",10,"bold"))
                activity_name.grid(column=0,row=current_row)
                view_details = tk.Button(inner_frame,text="View Activity Details",
                                           command = lambda n=name,d=details: show_activity_details(n,d))
                view_details.grid(row=current_row,column=1)
                current_row += 1
                best_modifier = max([kingdom.get_skill_modifier(skill) for skill in details["Skills"]])
                modifier_label = tk.Label(inner_frame,text="Best Modifier:")
                modifier_label.grid(row=current_row,column=0)
                modifier_value = tk.Label(inner_frame,text=str(best_modifier))
                modifier_value.grid(row=current_row,column=1)
                current_row += 1
                summary_label = tk.Label(inner_frame,text="Summary:")
                summary_label.grid(row=current_row,column=0)
                summary = tk.Label(inner_frame,text=details["Summary"],wraplength=300)
                summary.grid(row=current_row, column=1, columnspan=4,sticky="w")
                current_row += 1
                bottom_sep = ttk.Separator(inner_frame, orient="horizontal")
                bottom_sep.grid(column=0, columnspan=5, row=current_row, sticky="ew")
                current_row += 1
        vscroll = tk.Scrollbar(activities_search_frame,orient="vertical",command=activities_canvas.yview)
        vscroll.grid(row=0,column=1,rowspan=2000,sticky="ns")
        activities_canvas.configure(yscrollcommand=vscroll.set(0,0))
        activities_canvas.bind("<Configure>",
                              lambda e: activities_canvas.configure(scrollregion = activities_canvas.bbox("all")))
    draw_activities_list(general_activities)
