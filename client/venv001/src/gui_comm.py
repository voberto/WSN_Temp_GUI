### --------------------------------------- ###
### Name: gui_comm.py
### Author: voberto
### --------------------------------------- ###

# 1 - Imports
import gui_vars as gui_vars
import gui_log as gui_log

# 2 - Functions
# 2.1 - Check temperature command
def func_wsn001_check_temp_cmd(gui_client):
    gui_client.publish(gui_vars.mqtt_CmdTopic_var_start(), gui_vars.mqtt_TempCmd_var_start())

# 3 - Callback functions
# 3.1 - Callback for connection event
def callback_on_connect(client, userdata, flags, rc):
    # The callback for when the client receives a CONNACK response from the server.
    print("Trying to connect to the broker ...")
    
    gui_vars.LogBox.data_model.label_text_output += "\nTrying to connect to the broker ..."
    
    if rc == 0:
        print("Connected with broker", gui_vars.mqtt_BrokerAddress_var_start(), "\n")
        
        gui_vars.LogBox.data_model.label_text_output += "\nConnected with broker "
        gui_vars.LogBox.data_model.label_text_output += str(gui_vars.mqtt_BrokerAddress_var_start())
        gui_vars.LogBox.data_model.label_text_output += "\n"            
    
    # Subscribing in callback_on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    # Subscribing to 'temp' topic
    client.subscribe(gui_vars.mqtt_TempTopic_var_start())
    print("Subscribed to topic:", gui_vars.mqtt_TempTopic_var_start())

    gui_vars.LogBox.data_model.label_text_output += "Subscribed to topic: "
    gui_vars.LogBox.data_model.label_text_output += str(gui_vars.mqtt_TempTopic_var_start())
    gui_vars.LogBox.data_model.label_text_output += "\n"

    # Start MQTT loop
    print()
    client.loop_start()

# 3.2 - Callback for new message event
def callback_on_message(client, userdata, msg):
    # Decodes and returns message
    # When "True", print received messages in "log.txt"
    msg_out = gui_log.func_message_log(msg, True)
                        
    # Process data published in the 'temp' topic    
    if msg.topic == gui_vars.mqtt_TempTopic_var_start():
        gui_vars.TempLast_Value.last_temp_var = msg_out
        # Set flag to enable figure update
        gui_vars.TempNewArrived_Flag.new_temp_flag = True
            
# 3.3 - Callback for publish event
def callback_on_publish(client, userdata, mid):
    pass

# 3.4 - Callback for disconnection event
def callback_on_disconnect(client, userdata, rc):
    if rc != 0:
        print("\nUnexpected MQTT disconnection. Will reconnect ...")
        LogBox.data_model.label_text_output += "\nUnexpected MQTT disconnection. Will reconnect ..."
    client.loop_stop()
    client.connect(var_gui_mqtt_BrokerAdress, var_gui_mqtt_BrokerPort, var_gui_mqtt_BrokerTimeout)
