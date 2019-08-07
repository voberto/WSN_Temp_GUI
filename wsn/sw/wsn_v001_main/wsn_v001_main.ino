// #####################################################
// Project: 'esp8266-temp-sensor-with-gui' with NodeMCU, 
// mosquitto MQTT broker and DS18B20 sensor
//
// Author: voberto
//
// Description: ambient temperature is measured by the 
// DS18B20 sensor (pin D4)
// and sent to the MQTT broker 

// 1 - Include section
#include <string.h> 
#include <ESP8266WiFi.h> 
#include <DNSServer.h>            // Local DNS Server used for redirecting all requests to the configuration portal
#include <ESP8266WebServer.h>     // Local WebServer used to serve the configuration portal
#include <WiFiManager.h>          // WiFi Configuration Magic library
#include <PubSubClient.h> 

#include <OneWire.h>
#include <DallasTemperature.h>

// 2 - Defines section 
// 2.1 - Topics
#define BROKER_TOPIC_TEMP	"wsn/temp"	// Temperature readings
// 2.2 - Commands and answers    
#define WSN_TEMP_CMD		"WSN001_TEMP_CMD"
// 2.3 - MQTT ID
#define ID_MQTT  "USER"    
// 2.4 - NodeMCU pins
#define D0    16
#define D1    5
#define D2    4
#define D3    0
#define D4    2
#define D5    14
#define D6    12
#define D7    13
#define D8    15
#define D9    3
#define D10   1
#define ONE_WIRE_BUS        D4

// 3 - Variables declaration section
// 3.1 - Temperature variables
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);
char temperatureString[5];
// 3.2 - WIFI
const char* SSID 	    = "DEV-TEST";		      // TODO: change with your SSID's name
const char* PASSWORD 	= "d3vp@sZ_WSN";	    // TODO: change with your SSID's password  
// 3.3 - MQTT
const char* BROKER_MQTT = "192.168.25.5";	  // MQTT broker's IP
int BROKER_PORT = 1883;				              // MQTT broker's port
// 3.4 - Wifi and MQTT client objects  
WiFiClient espClient;              		      // espClient object
PubSubClient MQTT(espClient);			          // MQTT client's instance with espClient object

// 4 - Functions prototypes  
void Serial_Init();
void WiFi_Init();
void MQTT_Init();
void LED_Init(void);
void WiFi_Reconnect(); 
void MQTT_callback(char* topic, byte* payload, unsigned int length);
void ConnectionVerify(void);

// 5 - Functions declaration section
// 5.1 - Starts the serial communication peripheral 
void Serial_Init() 
{
    Serial.begin(115200);
    delay(10);
    Serial.println("\033[2J");      // Clear screen;
    Serial.println("\033[0;0H");    // Set cursor to 0,0;
    delay(10);
    Serial.println("Welcome to the \'WSN_Temp_GUI\' console!");
}
// 5.2 - Starts the Wifi peripheral 
void WiFi_Init() 
{
    Serial.print(" Starting connection to network called: ");
    Serial.println(SSID);
    Serial.println(" Wait ...");
     
    WiFi_Reconnect();
}
// 5.3 - Configure and init MQTT server and callback function  
void MQTT_Init() 
{
    MQTT.setServer(BROKER_MQTT, BROKER_PORT);   
    MQTT.setCallback(MQTT_callback);            
}

// 5.4 - Callback function for the MQTT system
void MQTT_callback(char* topic, byte* payload, unsigned int length) 
{
    String msg;
    for(int i = 0; i < length; i++) 
    {
       char c = (char)payload[i];
       msg += c;
    }
}

// 5.5 - MQTT reconnect function  
void MQTT_Reconnect() 
{
    while(!MQTT.connected()) 
    {
        Serial.print(" Trying to connect to the MQTT broker: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) 
        {
            Serial.println(" Successfully connected to the MQTT broker!");
            // Subscribes to the 'temp' topic
            Serial.println(" Subscribing to topic 'temp' ...");
            MQTT.subscribe(BROKER_TOPIC_TEMP);
            Serial.println(" Successfully subscribed to topic 'temp'!");
        } 
        else
        {
            Serial.println(" Failure on broker reconnection!");
            Serial.println(" New attempt of connection in 2s ... ");
            delay(2000);
        }
    }
}

// 5.6 - Reconnection function for the Wifi interface  
void WiFi_Reconnect() 
{
    if(WiFi.status() == WL_CONNECTED)
        return;
         
    WiFi.begin(SSID, PASSWORD);
     
    while(WiFi.status() != WL_CONNECTED) 
    {
        delay(100);
        Serial.print(".");
    }
   
    Serial.println();
    Serial.print(" Succesfully connected to the wireless network called ");
    Serial.println(SSID);
    Serial.print(" WSN_001 address: ");
    Serial.println(WiFi.localIP());
}
// 5.7 - Verify current connection 
void ConnectionVerify(void)
{
    if(!MQTT.connected()) 
    {    
    	MQTT_Reconnect(); 
    } 
    WiFi_Reconnect();
}
 
// 5.8 - Returns measured temperature
float Temperature_Measure() 
{
  float temp;
  do 
  {
  	DS18B20.requestTemperatures(); 
    	temp = DS18B20.getTempCByIndex(0);
    	delay(100);
  } 	
  while (temp == 85.0 || temp == (-127.0));
  return(temp);
}

// 5.9 - Converts and publishes temperature in the selected MQTT broker's topic
void Temperature_Publish()
{
    // Calls temp measurement function
    float temp = Temperature_Measure();
    // Converts float to string
    dtostrf(temp, 2, 2, temperatureString);
        
    // Publishes current temperature string in the 'temp' topic
    MQTT.publish(BROKER_TOPIC_TEMP, temperatureString);
    // Delays 1 second
    delay(1000);
}

// 6 - MAIN ROUTINES
// 6.1 - Main config function
void setup() 
{
    Serial_Init();
    //WiFiManager wifiManager;
    //wifiManager.autoConnect("DEV-TEST", "d3vp@sZ_WSN");    // TODO: change with your SSID's name and password
    WiFi_Init();
    MQTT_Init();
    DS18B20.begin();
    delay(100);
}
 
// 6.2 - Main loop
void loop() 
{   
    // Verify Wifi and broker connections
    ConnectionVerify();

    // Measure and send temperature to the broker
    Temperature_Publish();
 
    // MQTT broker's loop
    MQTT.loop();
}
