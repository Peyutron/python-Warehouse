/*
 * Programa asociado a gps adxl socket server:
 * https://github.com/Peyutron/python-Warehouse/tree/main/Sockets/gps_adxl_socket_server
 * 
 * Microcontrolador: ESP8266
 * Modo AP:
 * - SSID: gpsServer
 * - PASS: gps12345
 *
 * Sensores:
 * - ADXL345: https://github.com/adafruit/Adafruit_ADXL345
 * - NEO6MV2: https://github.com/mikalhart/TinyGPSPlus
 *
 * Toda la información sobre el proyecto:
 * https://www.infotronikblog.com/2024/11/esp8266-adxl345-y-openstreetmaps-con.html
 *
 * Software desarollado por Carlos Muñoz para https://www.infotronikblog.com
 * Fecha: 01/11/2024
 *
 */
 
 #include "ESP8266WiFi.h"

// Librerías para sensor ADXL_345
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

// Librerías para GPS6MV2
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

const char* ssid = "gpsServer";
const char* password =  "gps12345";
                         
WiFiServer wifiServer(1314);

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

/*
 * This sample code demonstrates the normal use of a TinyGPSPlus (TinyGPSPlus) object.
 * It requires the use of SoftwareSerial, and assumes that you have a
 * 4800-baud serial GPS device hooked up on pins (rx) and 3(tx).
 */
static const int RXPin = 0, TXPin = 2;
static const uint32_t GPSBaud = 9600;

// The TinyGPSPlus object
TinyGPSPlus gps;
boolean GPSWiringError = false;
String gpsdate = "";
String gpstime = "";

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

unsigned long previousMillis = 0;
const long interval = 1000;

unsigned long previousMillisError = 0;
const long intervalErrorGPS = 5000;


// Inicia el Serial, GPS NEO 6M V2 y comunicación como server

void setup() {
	Serial.begin(115200);
	
  delay(10);

	ss.begin(GPSBaud);
 
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  // Print ESP8266 Local IP Address
  Serial.println(WiFi.localIP());

  
  
  /* Initialise the sensor ADXL345 */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }

  /* Set the range to whatever is appropriate for your project */
  accel.setRange(ADXL345_RANGE_16_G);

  
  /* Display some basic information on this sensor */
  displaySensorDetails();
  
  /* Display additional settings (outside the scope of sensor_t) */
  displayDataRate();
  displayRange();
  Serial.println("");

    wifiServer.begin();

}

void loop() {


 WiFiClient client = wifiServer.available();
 
  if (client) {
    Serial.println("Client connected");
    while (client.connected())
    {
      client.print(getADXL());

      unsigned long currentMillis = millis();
      if (currentMillis - previousMillis >= interval) 
      {
        previousMillis = currentMillis;
        if(!GPSWiringError) client.print(neo6mv2data());
        Serial.println(neo6mv2data());
      }
      
      if ((currentMillis - previousMillisError >= intervalErrorGPS) && (gps.charsProcessed() < 10))
      {
        previousMillisError = currentMillis;
        GPSWiringError = true;
		    Serial.println(F("No GPS data received: check wiring"));
        client.print("<gps check wiring>");
      } else {
        if (gps.charsProcessed() > 10) GPSWiringError = false;
      }

      smartDelay(25);

  } // end client.connected
  client.stop();
  Serial.println("Client disconnected");
 
  } // end Client
}

// This custom version of delay() ensures that the gps object
// is being "fed".
static void smartDelay(unsigned long ms) {
	unsigned long start = millis();
	do {
		while (ss.available()) {
			gps.encode(ss.read());
		}
	} while (millis() - start < ms);
}
