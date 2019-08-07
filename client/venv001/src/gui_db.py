### ------------------------------------- ###
### Name: gui_db.py
### Author: voberto
### ------------------------------------- ###

# 1 - Imports
import numpy as np

# 2 - Functions
# 2.1 - Save data in the csv database (gui_db.csv)
def db1_csv_savedata(x,y):
    mat = np.column_stack((x,y))
    np.savetxt('gui_db.csv', mat, delimiter=",", fmt="%s")