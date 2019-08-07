### ------------------------------------- ###
### Name: gui_main.py
### Author: voberto
### ------------------------------------- ###

# 1 - Imports section
# 1.1 - General imports
import logging
# Disable WARNING messages
logging.disable(logging.WARNING)

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

# 1.2 - Specific project imports
import gui_vars as gui_vars
import gui_comm as gui_comm
import gui_plots as gui_plots

# 2 - Classes
# 2.1 - Tabbed panel as the main container for the GUI
class MainContainer(TabbedPanel):
    pass

# 2.2 - Main application
class GUI(App):
    # 1 - Initialization of some variables
    # 1.1 - MQTT client, broker's address, port and timeout
    var_gui_mqtt_client = gui_vars.mqtt_Client_var_start()
    var_gui_mqtt_BrokerAdress = gui_vars.mqtt_BrokerAddress_var_start()
    var_gui_mqtt_BrokerPort = gui_vars.mqtt_BrokerPort_var_start()
    var_gui_mqtt_BrokerTimeout = gui_vars.mqtt_BrokerTimeout_var_start()
    
    # 1.2 - Temperature buffer and flag
    temp_last_val = gui_vars.TempLast_Value()
    temp_new_arrived_flag = gui_vars.TempNewArrived_Flag()

    # 1.3 - Startup screen of the "fake" debug terminal (terminal)
    print("\nGreetings from the WSN_Temp_GUI debug console!")
        
    # 1.4 - Registering callbacks to handle connection, message receiving and publish MQTT events
    var_gui_mqtt_client.on_connect = gui_comm.callback_on_connect
    var_gui_mqtt_client.on_message = gui_comm.callback_on_message
    var_gui_mqtt_client.on_publish = gui_comm.callback_on_publish
    
    # 1.5 - Establish connection to the MQTT broker
    var_gui_mqtt_client.connect(var_gui_mqtt_BrokerAdress, var_gui_mqtt_BrokerPort, var_gui_mqtt_BrokerTimeout)

    # 1.6 - Start MQTT loop
    var_gui_mqtt_client.loop_start()
    
    # 1.7 - Build the graphical interface
    """ This class defines the application. """
    def build(self):
        # 1.7.1 - Loads Kivy GUI
        self.load_kv('gui_screen.kv')
        
        # 1.7.2 - Returns main widget    
        return MainContainer()

# 3 - Main routines
# 3.1 - Run the main application        
gui_App = GUI()
gui_App.run()