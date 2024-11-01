/*
 * Programa asociado a gps adxl socket server:
 * https://github.com/Peyutron/python-Warehouse/tree/main/Sockets/gps_adxl_socket_server
 * 
 * Microcontrolador: ESP8266
 * Modo cliente:
 * - SSID: your_ssid
 * - PASS: ssid_pass
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

const char* ssid = "your_ssid";
const char* password =  "your_ssid_pass";


WiFiServer wifiServer(1314);

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

/*
   This sample code demonstrates the normal use of a TinyGPSPlus (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   9600-baud serial GPS device hooked up on pins 0(rx) and 2(tx).
 */
static const int RXPin = 0, TXPin = 2;
static const uint32_t GPSBaud = 9600;
boolean GPSWiringError = false;
String gpsdate = "";
String gpstime = "";

// The TinyGPSPlus object
TinyGPSPlus gps;

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
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando..");
  }
 
  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());
 
  wifiServer.begin();
  // Inicia la comunicación con el módulo 
  Serial.println("Accelerometer Test"); Serial.println("");
  
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

  } // Fin client.connected
  client.stop();
  Serial.println("Client disconnected");
 
  } // Fin Client
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
