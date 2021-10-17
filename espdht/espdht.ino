#include <ESP8266WiFi.h>
#include <SPI.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>


#include "DHT.h"
#define DHTPIN D7    // what digital pin we're connected to
// Uncomment whatever type you're using!
#define DHTTYPE DHT11   // DHT 11


#define TLED D0 
#define HLED D5 

//esp connect to wifi
//const char* ssid = "hadeth";
//const char* pass = "Hadeth@@1400";

const char* ssid = "Aliali";
const char* pass = "alinote5";

String Url = "https://192.168.43.60:8000/iot/" ;
WiFiClient wifiClient;

DHT dht(DHTPIN, DHTTYPE);
void setup() {

  Serial.begin(9600);
  pinMode(HLED, OUTPUT);
  pinMode(TLED, OUTPUT);
  dht.begin();
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting");

  }
}




void loop() {

  float h = dht.readHumidity();
  int h_int = h * 1;
  float t = dht.readTemperature();
  int t_int = t * 1;

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    Serial.println("");
    Serial.println("Humidty: " + String(h_int) + " Temperature: " + String(t_int));

    String serverPath = Url + String(h_int) + "/" + String(t_int) ;
    http.begin(wifiClient, serverPath.c_str());
    int httpcode = http.GET();
    delay(1000);

    serverPath = Url + "getpidtdata";
    http.begin(wifiClient, serverPath.c_str());
    httpcode = http.GET();
    if (httpcode == 205) {
      Serial.println("everything is ok for temp!");
      analogWrite(TLED, 0);
    }
    else if (httpcode == 210) {
      Serial.println("manual mode led is on!");
      analogWrite(TLED, 255);
    }
    else if (httpcode == 211) {
      Serial.println("manual mode led is off!");
      analogWrite(TLED, 0);
    }
    else {
      httpcode = httpcode - 100 ;
      analogWrite(TLED, int(httpcode * 2.5));
      Serial.println("temperature control data: " + String(httpcode));
    }

    delay(1000);

    serverPath = Url + "getpidhdata";
    http.begin(wifiClient, serverPath.c_str());
    httpcode = http.GET();
    if (httpcode == 205) {
      Serial.println("everything is ok for humidity!");
      analogWrite(HLED, 0);
    }
    else if (httpcode == 210) {
      Serial.println("manual mode led is on!");
      analogWrite(HLED, 255);
    }
    else if (httpcode == 211) {
      Serial.println("manual mode led is off!");
      analogWrite(HLED, 0);
    }
    else {
      httpcode = httpcode - 100 ;
      analogWrite(HLED, int(httpcode * 2.5));
      Serial.println("humidity control data: " + String(httpcode));
    }

    http.end();

    delay(1000);

  }
}
