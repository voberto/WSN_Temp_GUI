### ------------------------------------ ###
### Name: gui_plots.py
### Author: voberto
### ------------------------------------ ###

# Imports section
# 1.1 - General imports
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from datetime import datetime
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as md
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import time

# 1.2 - Project-specific imports
import gui_vars as gui_vars
import gui_db as gui_db

# 2 - Variables
fig_temp = plt.figure()
ax1_temp = fig_temp.add_subplot(1,1,1)
xs_temp = []
ys_temp = []
temp_xaxis_max_ticks = 5
var_temp_last = 0
temp_x_vec_db = []
temp_y_vec_db = []
var_time_last = 0

# 3 - Functions
# 3.1 - Create animation for the plot with received temperature data 
def func_animate_temp(i):
    # If new data has arrived
    if gui_vars.TempNewArrived_Flag.new_temp_flag == True:
        global var_time_last
        global var_temp_last
        global temp_xaxis_max_ticks
        # Record current timestamp
        x_var = datetime.now()
        # Convert timestamp for each vector (plot and database)
        x_var_plot = matplotlib.dates.datestr2num(str(x_var))
        x_var_db = str(x_var.strftime("%H:%M:%S"))
        # Append data to each axis vector
        xs_temp.append(x_var_plot)
        ys_temp.append(float(gui_vars.TempLast_Value.last_temp_var))
        temp_x_vec_db.append(x_var_db)
        # Save data to database
        temp_y_vec_db.append(gui_vars.TempLast_Value.last_temp_var)
        gui_db.db1_csv_savedata(temp_x_vec_db, temp_y_vec_db)
        # Limit figure size by deleting vector elements when 
        # vector size is higher than "var_tempfig_maxlength" 
        var_tempfig_maxlength = 30
        if len(xs_temp) > var_tempfig_maxlength:
            xs_temp.pop(0)
            ys_temp.pop(0)
        ax1_temp.clear()
        # Specify maximum number of ticks on X axis
        locator = plt.MaxNLocator(temp_xaxis_max_ticks)
        ax1_temp.xaxis.set_major_locator(locator)
        # Specify legend format for X axis labels
        temp_xlabel_format = md.DateFormatter('%H:%M:%S')
        ax1_temp.xaxis.set_major_formatter(temp_xlabel_format)
        ax1_temp.grid(which='both')
        ax1_temp.set_title("Temperature")
        ax1_temp.set_ylabel("\u00b0C")
        ax1_temp.set_xlabel("Time")
        # Plot data
        ax1_temp.plot_date(xs_temp, ys_temp, marker='o', linestyle='-')
        gui_vars.TempNewArrived_Flag.new_temp_flag = False

# 4 - Classes
class PlotBox_temp(BoxLayout):
    def __init__(self, **kwargs):
        super(PlotBox_temp, self).__init__(**kwargs)
        # Set the animation update interval 
        temp_anim_interval_ms = 200
        # Add figure to canvas
        self.add_widget(FigureCanvasKivyAgg(figure=fig_temp))
        # Add animation to figure
        self.anim = animation.FuncAnimation(fig_temp, func_animate_temp, interval=temp_anim_interval_ms)
        # Set axis variables
        ax1_temp.set_title("Temperature")
        ax1_temp.set_ylabel("\u00b0C")
        ax1_temp.set_xlabel("Time")
        ax1_temp.grid(which='both')
        # Hide x-axis labels at plot startup 
        ax1_temp.set_xticklabels([])
        # First empty plot
        ax1_temp.plot_date(xs_temp, ys_temp, marker='o', linestyle='-')
