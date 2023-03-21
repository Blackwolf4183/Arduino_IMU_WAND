

void setup() {
  // Set software serial baud to 115200;

}

const int ledPin = 1; 

void callback(char *topic_received, byte *payload, unsigned int length) {


  //Send callback info to arduino nano
  if (!strcmp(topic_received, topic)) {
        if (!strncmp((char *)payload, "successful", length)) {
          //server accepted instruction
          digitalWrite(ledPin, HIGH); // LED on
          Serial.print("LED ON");
        } else if (!strncmp((char *)payload, "error", length)) {
          //something went wrong on server
          digitalWrite(ledPin, LOW); // LED OFF
          Serial.print("LED OFF");
        }
    }

}


void loop() {
  client.loop();     
  delay(100); 
  
}
