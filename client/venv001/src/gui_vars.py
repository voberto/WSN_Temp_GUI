### ------------------------------------- ###
### Name: gui_vars.py
### Author: voberto
### ------------------------------------- ###

# 1 - Imports
import paho.mqtt.client as mqtt
from kivy.properties import StringProperty
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# 2 - MQTT general variables protected by functions
def mqtt_Client_var_start():
    mqtt_Client = mqtt.Client()
    return mqtt_Client 

def mqtt_BrokerAddress_var_start():
    str_mqtt_BrokerAddress = "192.168.25.5"
    return str_mqtt_BrokerAddress

def mqtt_BrokerPort_var_start():    
    var_mqtt_BrokerPort = 1883
    return var_mqtt_BrokerPort

def mqtt_BrokerTimeout_var_start():    
    var_mqtt_BrokerTimeout = 60
    return var_mqtt_BrokerTimeout

def mqtt_TempTopic_var_start():
    # Topic to receive temperature values
    str_nodes_temp_Topic = "wsn/temp"
    return str_nodes_temp_Topic

# 3 - Strings for MQTT commands
def mqtt_TempCmd_var_start():
    str_temp_cmd = "WSN001_TEMP_CMD"
    return str_temp_cmd

# 4 - Classes for specific data shared between modules
class TempLast_Value(EventDispatcher):
    last_temp_var = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(TempLast_Value, self).__init__(*args, **kwargs)

class TempNewArrived_Flag(EventDispatcher):
    new_temp_flag = BooleanProperty()

    def __init__(self, *args, **kwargs):
        super(TempNewArrived_Flag, self).__init__(*args, **kwargs)

class DataModel(EventDispatcher):
    label_text_output = StringProperty('')

    def __init__(self, *args, **kwargs):
        super(DataModel, self).__init__(*args, **kwargs)

class LogBox(Widget):
    """ This class inherits Widget properties. """
    data_model = DataModel()

    data_model.label_text_output = "Greetings from WSN_Temp_GUI log console!"

