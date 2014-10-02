// simple, incomplete REST interface for getting DHT sensor values

/*
 * Request:
 *
 * GET /sensorData HTTP/1.1\r\n
 * [gets ignored]\n
 * [gets ignored]\n
 *
 * Response:
 *
 * HTTP/1.1 200 OK\n
 * Content-Type: application/json\n
 * {
 * "humidity": xx.x,
 * "temperature": xx.x,
 * "luminosity": xx.x
 * }
 * \n
 *
 */
 

#include "DHT.h"

#include <SPI.h>
#include <Ethernet.h>

#define DHT_PIN         A2
#define TEMP_PIN       A0
#define PHOTOCELL_PIN  A4

#define DHTTYPE DHT11   // DHT 11 

DHT dht(DHT_PIN, DHTTYPE);

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
EthernetServer server(80);

EthernetClient client;
String ethernetBuffer;

char c;
int maxLengthCounter = 0;

int requestState = 0;

float hum = 0;
float temp = 0;
float lum = 0;

void setup() {
  Serial.begin(9600);
 
  dht.begin();
  
  Ethernet.begin(mac);
  server.begin();
}

void loop() {
  etherEvent();
}

unsigned int updateSensorData() {
  float hum_tmp = dht.readHumidity();

  delay(10);
  analogRead(TEMP_PIN); // switch the ADC multiplexer and give it some time
  delay(20);
  float temp_tmp = (5.0 * analogRead(TEMP_PIN) * 100.0) / 1024;
  delay(10);
  float lum_tmp = analogRead(PHOTOCELL_PIN);

  if (isnan(temp_tmp) || isnan(hum_tmp)) {
    return 1;
  } else {
    hum = hum_tmp;
    temp = temp_tmp;
    lum = lum_tmp;
    return 0;
  }
}

void etherEvent() {
  if (!client) {
    client = server.available();
  } else {
    if (client.connected()) {
      if (client.available()) { // while würde hier blocken
        c = client.read();
        
        Serial.print(c);
        
        if (c == '\n') { // sollte eigentlich <CR><LF> sein
          triggerEtherCommand();          
        } else {
          ethernetBuffer += c;
          maxLengthCounter++;
        }
        
        if (maxLengthCounter > 100) {
          client.println("ERROR command length exceeded");
          closeConnection();
        }
        
      }
    } else {
      closeConnection();
    }
  }
}

void triggerEtherCommand() {
  
  switch (requestState) {
    case 0:
      if (ethernetBuffer == "GET /sensorData HTTP/1.1\r") {
        requestState = 1;
      } else {
        requestState = 0;
        sendNegativeResponse();
      }
      break;
    case 1:
      requestState = 2;
      break;
    case 2:
      sendPositiveResponse();
      requestState = 0;
      break;
  }
  
  maxLengthCounter = 0;
  ethernetBuffer = "";

  // if no command was recognized
  // printERROR();
}

void sendPositiveResponse() {
  
  if (updateSensorData() != 0) {
    sendNegativeResponse();
    return;
  }
  
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println();
  client.println("{");
  client.print("\x22humidity\x22: "); // \x22 = "
  client.print(hum);
  client.println(",");
  client.print("\x22temperature\x22: ");
  client.println(temp);    
  client.println(",");
  client.print("\x22luminosity\x22: ");
  client.println(lum);    
  client.println("}");
  closeConnection();
}

void sendNegativeResponse() {
  client.println("HTTP/1.1 500 Internal Error");
  client.println("Content-Type: text/html");
  client.println();
  client.println("error");
  closeConnection();
}

void closeConnection() {
  maxLengthCounter = 0;
  ethernetBuffer = "";
  // give the client time to receive the data
  delay(1);
  // close the connection:
  client.stop();
}

void printOK() {
  client.println("OK");
}

void printERROR() {
  client.println("ERROR");
}

void printERROR(String str) {
  client.print("ERROR ");
  client.println(str);
}
