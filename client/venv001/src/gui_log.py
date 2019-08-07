### --------------------------------------- ###
### Name: gui_log.py
### Author: voberto
### --------------------------------------- ###

# 1 - Imports
import gui_vars as gui_vars

# 2 - Functions
# 2.1 - Output received message and save data to the log.txt file
def func_message_log(k, print_enabled_flag):
    msg_dec = k.payload.decode('ascii')
    
    if print_enabled_flag == True:
        print("\nData received! \nTopic:", k.topic, "\nMessage:", msg_dec)
        print()
    
        msg_save = open('log.txt', 'w')    

        gui_vars.LogBox.data_model.label_text_output += "\nReceived message!"
        gui_vars.LogBox.data_model.label_text_output += "\nTopic: "
        gui_vars.LogBox.data_model.label_text_output += str(k.topic)
        gui_vars.LogBox.data_model.label_text_output += "\nMessage: "
        gui_vars.LogBox.data_model.label_text_output += str(msg_dec)
        gui_vars.LogBox.data_model.label_text_output += "\n"
        
        msg_save.write(gui_vars.LogBox.data_model.label_text_output)
        msg_save.close()

    return msg_dec
