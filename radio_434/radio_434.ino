#include <SPI.h>
#include <Ethernet.h>

byte mac[] = {0xDE, 0xED, 0xBA, 0xEE, 0xFE, 0xEA};

EthernetServer server(8282);

EthernetClient client;
String ethernetBuffer;

char c;
int maxLengthCounter = 0;

#define SWITCHON  "10"
#define SWITCHOFF "01"

#define SENDER_DATA_PIN A0

// 10101       00100     10       x
// house code  receiver  command  sync

void setup() {
  pinMode(SENDER_DATA_PIN, OUTPUT);
  
  Ethernet.begin(mac);
  server.begin();
  
  Serial.begin(9600);
}

void loop() {
  if (!client) {
    client = server.available();
  } else {
    if (client.connected()) {
      if (client.available()) {
        c = client.read();
        
        // Serial.print(c);
        
        if (c == '\n') { // although it should probably be <CR><LF> 
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
  if (ethernetBuffer.substring(0,4) == "SEND") {
    sendCode(ethernetBuffer.substring(5));
  }
  
  maxLengthCounter = 0;
  ethernetBuffer = "";
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
 
boolean sendCode(String code){
  for(short z = 0; z<7; z++){ // repeat the code 7x
    for(short i = 0; i<12; i++){ // codelength 12 bits
      sendByte(code[i]);
    }
  sendByte('x'); // send sync code
  }
}
 
void sendByte(char i) {
  switch(i){
  case '0':{
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1); 
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(1);
    return;
  }
  case '1':{ 
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    return;
  }
  case 'x':{
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(31);
  }
  }
}
 
void wait(int x) {
  delayMicroseconds(x*350); // wait x*350us
}
